#! /usr/bin/env python3
# coding: utf-8

from math import log10

from classes.query import Query


class BM25:

    def __init__(self, reuters, index, n, k1=0.5, b=0.5):
        """
        Initialize the Okapi BM25 (Best Matching) ranking function.

        :param reuters: Reuters object which will contain relevant information such as document length, average length.
        :param index: dictionary with terms as keys, and their postings list as values.
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
        self.index = index
        self.N = n
        self.K1 = k1
        self.B = b
        self.average_document_length = reuters.average_document_length

    def get_document_frequency(self, term):
        """
        Call the get_postings_list method of the Query class, and return its length.
        :param term: the term we want the frequency of.
        :return: the number of documents the term appears in.
        """
        postings_list = Query(self.index).get_postings_list_of_one_term(term)
        return len(postings_list)

    def get_idf_weight(self, term):
        dft = self.get_document_frequency(term)
        return log10(self.N / dft)
