#! /usr/bin/env python3
# coding: utf-8

from reuters import Reuters
from spimi import SPIMI
from query import Query, AndQuery, OrQuery
import argparse


parser = argparse.ArgumentParser(description="Configure Reuters parser and set block size limit.")

parser.add_argument("-mb", "--max-block-size", type=float, help="max block size", default=1)
parser.add_argument("-rs", "--remove-stopwords", action="store_true", help="remove stopwords", default=False)
parser.add_argument("-s", "--stem", action="store_true", help="stem terms", default=False)
parser.add_argument("-c", "--case-folding", action="store_true", help="use case folding", default=False)
parser.add_argument("-rn", "--remove-numbers", action="store_true", help="remove numbers", default=False)

args = parser.parse_args()


if __name__ == '__main__':
    print(args)
    reuters = Reuters(remove_stopwords=True, stem=True, case_folding=True, remove_numbers=True)

    spimi = SPIMI(
        reuters=reuters,
        output_directory="DISK", output_index="index",
        block_prefix="BLOCK", max_block_size=1
    )

    index = spimi.construct_index()

    OrQuery(index, "updat upgrad").execute()
    AndQuery(index, "coke year").execute()
    AndQuery(index, "rubber rice reuter").execute()
    AndQuery(index, "and you").execute()
    Query(index, "wale").execute()
    AndQuery(index, "hard").execute()
