#! /usr/bin/env python3
# coding: utf-8

from beautifultable import BeautifulTable
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import random


class CompressionTable:

    def __init__(self, index):
        """
        Initialize original index and its filtered counterparts to be filled later.
        Initialize 2 sets of stopwords: one containing 30, the other containing 150, chosen at random.
        Initialize the Porter stemmer which will be used to stem terms.
        Initialize the table and its headers with BeautifulTable.

        :param index: index used as the unfiltered version, which will be filtered using various methods.
        """
        self.index = index

        self.index_no_numbers = {}
        self.index_case_folding = {}
        self.index_remove_30_stopwords = {}
        self.index_remove_150_stopwords = {}
        self.index_stem = {}

        self.stopwords = set(stopwords.words("english"))
        self.stopwords = random.sample(self.stopwords, 150)
        self.stopwords_30 = list(self.stopwords)[:30]
        self.stopwords_150 = list(self.stopwords)[:150]

        self.ps = PorterStemmer()

        self.table = BeautifulTable()
        self.table.column_headers = ["", "# distinct terms", "∆ % from previous", "∆ % from unfiltered"]

    def generate_table(self):
        """
        Append table with relevant information.
        :return: table fully populated.
        """
        self.table.append_row(self.get_unfiltered())
        self.table.append_row(self.get_no_numbers())
        self.table.append_row(self.get_case_folding())
        self.table.append_row(self.get_without_30_stopwords())
        self.table.append_row(self.get_without_150_stopwords())
        return self.table

    def get_unfiltered(self):
        """
        Do nothing to index.
        :return: row featuring information on original index.
        """
        return ["unfiltered", "{:,}".format(len(self.index)), "-", "-"]

    def get_no_numbers(self):
        """
        Take out terms that are just numbers.
        Given a term, once we take out all commas & periods, if it's just a string of digits, it's considered a number.
        :return: row featuring information on index without numbers.
        """
        self.index_no_numbers = {term: postings for term, postings in self.index.items() if not term.replace(",", "").replace(".", "").isdigit()}

        reduction_from_previous = self.get_reduction_percentage(self.index, self.index_no_numbers)
        total_reduction = reduction_from_previous

        return ["no numbers", "{:,}".format(len(self.index_no_numbers)), reduction_from_previous, total_reduction]

    def get_case_folding(self):
        """
        Make all terms lowercase.
        :return: row featuring information on index with all terms lowercased.
        """
        for term in self.index_no_numbers.keys():
            if term.casefold() not in self.index_case_folding.keys():
                self.index_case_folding[term.casefold()] = self.index_no_numbers[term]
            else:
                self.index_case_folding[term.casefold()].extend(self.index_no_numbers[term])

        reduction_from_previous = self.get_reduction_percentage(self.index_no_numbers, self.index_case_folding)
        total_reduction = self.get_reduction_percentage(self.index, self.index_case_folding)

        return ["case folding", "{:,}".format(len(self.index_case_folding)), reduction_from_previous, total_reduction]

    def get_without_30_stopwords(self):
        """
        Take out 30 stopwords from the index.
        :return: row featuring information on index with 30 stopwords taken out.
        """
        self.index_remove_30_stopwords = {term: postings for term, postings in self.index_case_folding.items() if term.lower() not in self.stopwords_30}

        reduction_from_previous = self.get_reduction_percentage(self.index_case_folding, self.index_remove_30_stopwords)
        total_reduction = self.get_reduction_percentage(self.index, self.index_remove_30_stopwords)

        return ["30 stopwords", "{:,}".format(len(self.index_remove_30_stopwords)), reduction_from_previous, total_reduction]

    def get_without_150_stopwords(self):
        """
        Take out 150 stopwords from the index.
        :return: row featuring information on index with 150 stopwords taken out.
        """
        self.index_remove_150_stopwords = {term: postings for term, postings in self.index_remove_30_stopwords.items() if term.lower() not in self.stopwords_150}

        reduction_from_previous = self.get_reduction_percentage(self.index_remove_30_stopwords, self.index_remove_150_stopwords)
        total_reduction = self.get_reduction_percentage(self.index, self.index_remove_150_stopwords)

        return ["150 stopwords", "{:,}".format(len(self.index_remove_150_stopwords)), reduction_from_previous, total_reduction]

    def get_stemmed(self):
        """
        Stem all terms.
        :return: row featuring information on index with all terms stemmed.
        """
        self.index_stem = {term: postings for term, postings in self.index_remove_150_stopwords}

    @staticmethod
    def get_reduction_percentage(bigger_index, smaller_index):
        """
        Get difference in size between 2 indexes.
        :param bigger_index: index containing the larger amount of terms.
        :param smaller_index: index containing the smaller amount of terms.
        :return: difference in size between both indexes, given in percentage (%), rounded to nearest 2 decimals.
        """
        reduction_percentage = (len(bigger_index) - len(smaller_index))/len(bigger_index) * 100
        return "{0:.2f}".format(reduction_percentage)
