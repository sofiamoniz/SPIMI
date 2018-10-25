#! /usr/bin/env python3
# coding: utf-8

import abc

from definitions import word_tokenize, ps


class Query:

    def __init__(self, index, terms):
        """
        Query constructor.
        :param index: dictionary with terms as keys, and their postings list as values.
        :param terms: query which will be conducted, all stemmed
        """
        self.index = index
        self.original_terms = terms.split()
        self.terms = [ps.stem(term) for term in word_tokenize(terms)]

    @staticmethod
    def ask_user():
        query = input("Type in a search query.\n")
        print()
        return query

    def get_postings_lists(self):
        """
        Split the query into individual terms.
        For each terms, store in a dictionary the documents in which the term appears (postings list).
        :return: list of postings lists found from the terms in the query.
        """
        results = {}

        for term in self.terms:
            try:
                results[term] = self.index[term]
            except KeyError:
                results[term] = []

        return list(results.values())

    @abc.abstractmethod
    def execute(self):
        """
        Abstract method, to be implemented by subclasses.
        If run by parent class, will print out message pointing out error.
        :return: None
        """
        if self.__class__.__name__ == "Query":
            print("You are conducting a query using the %s class." % self.__class__.__name__)
            print("Make sure to use either AndQuery or OrQuery.\n")
        return

    def print_results(self, results):
        """
        Print out terms in the query, and the postings found.
        :param results: list of postings.
        """
        if results:
            print("%s (original): %s" % (self.__class__.__name__, " ".join(self.original_terms)))
            print("%s (stemmed): %s" % (self.__class__.__name__, " ".join(self.terms)))
            print("%s result(s) found: %s\n" % ("{:,}".format(len(results)), ", ".join(map(str, results))))
        else:
            print("Your search didn't return any results.\n")


class AndQuery(Query):

    def __init__(self, index, terms):
        Query.__init__(self, index, terms)

    def execute(self):
        """
        Get postings lists and conduct their intersection.
        :return: postings list for a query using conjunction (and).
        """
        postings_lists = self.get_postings_lists()

        try:
            results = sorted(set(postings_lists[0]).intersection(*[set(postings_list) for postings_list in postings_lists[1:]]))
        except IndexError:
            results = []

        self.print_results(results)


class OrQuery(Query):

    def __init__(self, index, terms):
        Query.__init__(self, index, terms)

    def execute(self):
        """
        We get a list of postings lists at first.
        We want to make a flat list from each one of these lists.

        We want to eliminate duplicates, but by keeping the postings that appear the most often at the beginning of the
        list. We do this by initializing an empty set, and seeing which elements of the postings list appears the most.
        If it's not in the set, we add it. We repeat until there are no more elements in the initial list to go over.

        :return: postings list for a query, with postings matching the most query terms are the beginning of the list.
        """
        postings_lists = self.get_postings_lists()
        postings_lists = [posting for postings_list in postings_lists for posting in postings_list]

        postings_lists = sorted(postings_lists, key=lambda x: (postings_lists.count(x), -x), reverse=True)

        postings_lists_set = set()
        postings_lists_set_add = postings_lists_set.add

        results = [posting for posting in postings_lists if not (posting in postings_lists_set or postings_lists_set_add(posting))]

        self.print_results(results)
