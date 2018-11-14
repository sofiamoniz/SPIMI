#! /usr/bin/env python3
# coding: utf-8

from math import log10
from operator import itemgetter

from definitions import ps, word_tokenize
from classes.query import Query, OrQuery


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

        The equation we will model is the following:
        ∑ (for term in query) [ log10(N / df_t) * ( (k1 + 1)tf_td / (k1((1 - b) + b * (L_d / L_ave)) + tf_td) ) ]
        """
        self.reuters = reuters
        self.index = index
        self.Query = Query(self.index)

        self.N = n
        self.K1 = k1
        self.B = b

        self.document_lengths = self.reuters.document_lengths
        self.L_ave = self.reuters.average_document_length

    def get_documents_of_term(self, term):
        return set(self.Query.get_postings_list_of_one_term(term))

    def get_document_frequency(self, term):
        """
        Call the get_postings_list method of the Query class, and return its length.
        :param term: the term we want the frequency of.
        :return: the number of documents the term appears in, or df_t.
        """
        try:
            postings_list = self.index[ps.stem(term)]
            return len(set(postings_list))
        except KeyError:
            return 0

    def get_frequency_of_term_in_doc(self, term, doc_id):
        """
        Count the number of times a certain document ID appears in a term's postings list.
        :param term: the term.
        :param doc_id: the document we're looking at.
        :return: the number of times the term appears in the document.
        """
        try:
            postings_list = self.index[ps.stem(term)]
            return postings_list.count(doc_id)
        except KeyError:
            return 0

    def compute_idf_weight(self, term):
        """
        Get the inverse document frequency weight of a term.
        :param term: the term.
        :return: its inverse document frequency weight, or idf.
        """
        dft = self.get_document_frequency(term)
        try:
            return log10(self.N / dft)
        except ZeroDivisionError:
            return 0

    def compute_numerator(self, term, doc_id):
        return (self.K1 + 1) * self.get_frequency_of_term_in_doc(term, doc_id)

    def compute_denominator(self, term, doc_id):
        return self.K1 * ((1 - self.B) + self.B * (self.document_lengths[doc_id] / self.L_ave)) + self.get_frequency_of_term_in_doc(term, doc_id)

    def compute_bm25(self, query):
        """
        Compute the Okapi BM25 ranking formula to rank retrieved documents by relevance.
        :param query: query to be conducted.
        """
        doc_ids = OrQuery(self.index).execute(query)
        terms = [ps.stem(term) for term in word_tokenize(query)]
        rank = {}

        for doc_id in doc_ids:
            score = 0
            for term in terms:
                score += self.compute_idf_weight(term) * self.compute_numerator(term, doc_id) / self.compute_denominator(term, doc_id)
            rank[doc_id] = score

        sorted_rank = sorted(rank.items(), key=itemgetter(1), reverse=True)

        print("{} documents found.".format(len(doc_ids)))
        for k, v in sorted_rank:
            print("Document {} score: {}".format(k, v))
        print()
