#! /usr/bin/env python3
# coding: utf-8

import abc

from definitions import word_tokenize, ps


class Query:

    def __init__(self, index):
        """
        Query constructor.
        :param index: dictionary with terms as keys, and their postings list as values.
        """
        self.index = index
        self.original_terms = ""
        self.terms = []

        self.most_recent_results = []

    @staticmethod
    def ask_user():
        query = input("Type in a search query.\n")
        print()
        return query

    def get_postings_list_of_one_term(self, term):
        """
        Get a term's postings list, i.e. list of document ID's of documents that it's in.
        :param term: the term.
        :return: list of doc IDs.
        """
        try:
            return self.index[ps.stem(term)]
        except KeyError:
            return []

    def get_postings_lists(self, terms):
        """
        Split the query into individual terms.
        For each terms, store in a dictionary the documents in which the term appears (postings list).
        :param: the user's query.
        :return: list of postings lists found from the terms in the query.
        """
        self.original_terms = terms
        self.terms = [ps.stem(term) for term in word_tokenize(terms)]

        results = {}

        for term in self.terms:
            try:
                results[term] = self.index[term]
            except KeyError:
                results[term] = []

        return list(results.values())

    @abc.abstractmethod
    def execute(self, terms):
        """
        Abstract method, to be implemented by subclasses.
        If run by parent class, will print out message pointing out error.
        :param terms: the user's query.
        :return: None
        """
        if self.__class__.__name__ == "Query":
            print("You are conducting a query using the %s class." % self.__class__.__name__)
            print("Make sure to use either AndQuery or OrQuery.\n")
        return

    def print_results(self):
        """
        Print out terms in the query, and the postings found.
        :param results: list of postings.
        """
        if self.most_recent_results:
            print("%s (original): %s" % (self.__class__.__name__, self.original_terms))
            print("%s (stemmed): %s" % (self.__class__.__name__, " ".join(self.terms)))
            print("%s result(s) found: %s\n" % ("{:,}".format(len(self.most_recent_results)), ", ".join(map(str, self.most_recent_results))))
        else:
            print("Your search didn't return any results.\n")


class AndQuery(Query):

    def __init__(self, index):
        Query.__init__(self, index)

    def execute(self, terms):
        """
        Get postings lists and conduct their intersection.
        :param terms: the user's query.
        :return: postings list for a query using conjunction (and).
        """
        postings_lists = self.get_postings_lists(terms)

        try:
            self.most_recent_results = sorted(set(postings_lists[0]).intersection(*[set(postings_list) for postings_list in postings_lists[1:]]))
        except IndexError:
            self.most_recent_results = []

        return self.most_recent_results


class OrQuery(Query):

    def __init__(self, index):
        Query.__init__(self, index)

    def execute(self, terms):
        """
        We get a list of postings lists at first.
        We want to make a flat list from each one of these lists.

        We want to eliminate duplicates, but by keeping the postings that appear the most often at the beginning of the
        list. We do this by initializing an empty set, and seeing which elements of the postings list appears the most.
        If it's not in the set, we add it. We repeat until there are no more elements in the initial list to go over.

        :param terms: the user's query.

        :return: postings list for a query, with postings matching the most query terms are the beginning of the list.
        """
        postings_lists = self.get_postings_lists(terms)
        postings_lists = [posting for postings_list in postings_lists for posting in postings_list]

        postings_lists = sorted(postings_lists, key=lambda x: (postings_lists.count(x), -x), reverse=True)

        postings_lists_set = set()
        postings_lists_set_add = postings_lists_set.add

        self.most_recent_results = [posting for posting in postings_lists if not (posting in postings_lists_set or postings_lists_set_add(posting))]

        return self.most_recent_results
