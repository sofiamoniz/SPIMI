#! /usr/bin/env python3
# coding: utf-8

from definitions import ps
from classes.reuters import Reuters
from classes.spimi import SPIMI
from classes.query import Query, AndQuery, OrQuery
from classes.compression_table import CompressionTable
from classes.bm25 import BM25

import argparse


def stem_index(index):
    """
    We will use this method to convert all index keys to lowercase, which will produce more consistent results when we
    conduct queries.
    Note: This is only used for the queries. The index that appears in the index.txt file hasn't been modified.

    :param index: dictionary containing terms and the postings in which they appear.

    :return: index with all keys stemmed, making sure the postings combine as well. For example:
    {'hello': [1, 2], 'Hello': [1, 3], 'HELLO': [2, 3, 5]} would return a dictionary of: {'hello': [1, 2, 3, 5]}.
    """
    new_index = {}
    for k, v in index.items():
        if ps.stem(k) not in new_index.keys():
            new_index[ps.stem(k)] = index[k]
        else:
            new_index[ps.stem(k)] = new_index[ps.stem(k)] + index[k]

    return new_index


parser = argparse.ArgumentParser(description="Configure Reuters parser and set document limit per block.")

parser.add_argument("-d", "--docs", type=int, help="documents per block", default=500)
parser.add_argument("-r", "--reuters", type=int, help="number of Reuters files to parse, choice from 1 to 22", choices=range(1, 23), default=22)
parser.add_argument("-rs", "--remove-stopwords", action="store_true", help="remove stopwords", default=False)
parser.add_argument("-s", "--stem", action="store_true", help="stem terms", default=False)
parser.add_argument("-c", "--case-folding", action="store_true", help="use case folding", default=False)
parser.add_argument("-rn", "--remove-numbers", action="store_true", help="remove numbers", default=False)
parser.add_argument("-a", "--all", action="store_true", help="use all compression techniques", default=False)

args = parser.parse_args()


if __name__ == '__main__':

    if args.all:
        args.remove_stopwords = True
        args.stem = True
        args.case_folding = True
        args.remove_numbers = True

    """
    Upon initialization, downloads Reuters files if they're not downloaded, and stores them in a list.
    """
    reuters = Reuters(
        number_of_files=args.reuters,
        docs_per_block=args.docs,
        remove_stopwords=args.remove_stopwords,
        stem=args.stem,
        case_folding=args.case_folding,
        remove_numbers=args.remove_numbers
    )

    """
    Upon initialization, makes the Reuters object tokenize the files mentioned above, and stores them in a variable.
    Also creates the output directory if it hasn't been initialized.
    """
    spimi = SPIMI(reuters=reuters)

    index = spimi.construct_index()

    if args.remove_stopwords or args.stem or args.case_folding or args.remove_numbers:
        print("Your index has already been compressed, will use that as unfiltered.")

    table = CompressionTable(index)
    print(table.generate_table())
    print()

    """
    Stemming every term in the index so that it's easy to compare them in queries.
    Queries will also be stemmed.
    Google, for example, uses this technique in their search engine.
    """
    if not args.stem:
        index = stem_index(index)

    """
    Allow user to conduct queries.
    First, ask if they want AND or OR query.
    Then, prompt them for the desired query.
    After outputting results, repeat.
    """
    while True:
        user_input = input("Would you like to conduct an AND query or an OR query? Hit enter to end the program. [and/or] ")
        if user_input == "":
            break
        elif user_input.lower() in ["and", "or"]:
            and_query = AndQuery(index)
            or_query = OrQuery(index)
            user_query = Query.ask_user()
            if user_input.lower() == "and":
                and_query.execute(user_query)
            elif user_input.lower() == "or":
                or_query.execute(user_query)

    bm25 = BM25(reuters=reuters, index=index, n=reuters.number_of_documents)
