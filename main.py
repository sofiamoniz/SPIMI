#! /usr/bin/env python3
# coding: utf-8

from classes.reuters import Reuters
from classes.spimi import SPIMI
from classes.query import Query, AndQuery, OrQuery, ask_user
from classes.compression_table import CompressionTable
import argparse

from time import time


parser = argparse.ArgumentParser(description="Configure Reuters parser and set block size limit.")

parser.add_argument("-docs", "--docs-per-block", type=int, help="documents per block", default=500)
parser.add_argument("-r", "--reuters", type=int, help="number of Reuters files to parse", choices=range(1, 23), default=22)
parser.add_argument("-rs", "--remove-stopwords", action="store_true", help="remove stopwords", default=False)
parser.add_argument("-s", "--stem", action="store_true", help="stem terms", default=False)
parser.add_argument("-c", "--case-folding", action="store_true", help="use case folding", default=False)
parser.add_argument("-rn", "--remove-numbers", action="store_true", help="remove numbers", default=False)

args = parser.parse_args()


if __name__ == '__main__':

    start = time()

    reuters = Reuters(
        number_of_files=args.reuters,
        docs_per_block=args.docs_per_block,
        remove_stopwords=args.remove_stopwords,
        stem=args.stem,
        case_folding=args.case_folding,
        remove_numbers=args.remove_numbers
    )

    spimi = SPIMI(
        reuters=reuters,
        output_directory="DISK", block_prefix="BLOCK", output_index="index",
    )

    tokenize = time()
    print("%s seconds to tokenize." % "{0:.3f}".format((tokenize - start)))

    index = spimi.construct_index()

    construct_index = time()
    print("%s seconds to construct inverted index." % "{0:.3f}".format((construct_index - tokenize)))

    if args.remove_stopwords or args.stem or args.case_folding or args.remove_numbers:
        print("Your index has already been compressed, will use that as unfiltered.")

    table = CompressionTable(index)
    print(table.generate_table())
    print()

    generate_table = time()
    print("%s seconds to generate statistics table." % "{0:.3f}".format((generate_table - construct_index)))

    print("%s seconds to completion.\n" % "{0:.3f}".format((time() - start)))

    while True:
        user_input = input("Would you like to conduct an AND query or an OR query? Hit enter to end the program. ")
        if user_input == "":
            break
        elif user_input.lower() in ["and", "or"]:
            user_query = ask_user()
            if user_input.lower() == "and":
                AndQuery(index, user_query).execute()
            elif user_input.lower() == "or":
                OrQuery(index, user_query).execute()
