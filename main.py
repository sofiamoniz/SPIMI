#! /usr/bin/env python3
# coding: utf-8

from get_reuters import *
from reuters_tokens import *
from spimi import *


if __name__ == '__main__':
    reuters_files = get_reuters_files()
    tokens = get_tokens(reuters_files[:1], remove_stopwords=True, stem=True)

    spimi = SPIMI(tokens=tokens, output_directory="DISK", output_index="index", block_size_limit=1)
    index = spimi.construct_index()
