#! /usr/bin/env python3
# coding: utf-8

from get_reuters import *
from reuters_tokens import *
from spimi import *


if __name__ == '__main__':
    reuters_files = get_reuters_files()
    tokens = get_tokens(reuters_files[:1], remove_stopwords=True, stem=True)

    spimi = SPIMI(tokens, "DISK", 1)
    block_files = spimi.create_inverted_index()
    print(block_files)
