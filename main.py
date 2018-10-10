#! /usr/bin/env python3
# coding: utf-8

from get_reuters import *
from reuters_tokens import *
from spimi import *
from query import *


if __name__ == '__main__':
    spimi = SPIMI(output_directory="DISK", output_index="index", block_size_limit=1, remove_stopwords=False, stem=False)
    index = spimi.construct_index()

    OrQuery(index, "updat upgrad").execute()
    AndQuery(index, "coke year").execute()
    AndQuery(index, "rubber rice reuter").execute()
    AndQuery(index, "and you").execute()
    Query(index, "wale").execute()
    AndQuery(index, "hard").execute()
