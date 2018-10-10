#! /usr/bin/env python3
# coding: utf-8

from reuters import Reuters
from spimi import SPIMI
from query import Query, AndQuery, OrQuery


if __name__ == '__main__':
    reuters = Reuters(remove_stopwords=False, stem=False)

    spimi = SPIMI(
        reuters=reuters,
        output_directory="DISK", output_index="index",
        block_prefix="EXAMPLE", block_size_limit=1
    )

    index = spimi.construct_index()

    OrQuery(index, "updat upgrad").execute()
    AndQuery(index, "coke year").execute()
    AndQuery(index, "rubber rice reuter").execute()
    AndQuery(index, "and you").execute()
    Query(index, "wale").execute()
    AndQuery(index, "hard").execute()
