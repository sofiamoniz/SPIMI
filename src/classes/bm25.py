#! /usr/bin/env python3
# coding: utf-8

from math import log10

class BM25:

    def __init__(self, n, k1=0.5, b=0.5):
        """
        Initialize the Okapi BM25 (Best Matching) ranking function.

        :param n: Number of documents in the collection.
        :param k1: Positive parameter used to scale the document frequency scaling.
                   k1 = 0 corresponds to a binary model (no term frequency).
        :param b: 0 ≤ b ≤ 1. Used to determine the scaling by document length.
                  b = 1 corresponds to fully scaling the term weight by the document length.
                  b = 0 corresponds to no length normalization.

        This information has been taking from the textbook:
            - An Introduction to Information Retrieval, by:
                Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze
        """
        self.N = n
        self.K1 = k1
        self.B = b
