#! /usr/bin/env python3
# coding: utf-8

import abc


class Query:

    def __init__(self, index, terms):
        """
        Query constructor.
        :param index: dictionary with terms as keys, and their postings list as values.
        :param terms: query which will be conducted
        """
        self.index = index
        self.terms = terms.split()

    def get_postings_lists(self):
        """
        Split the query into individual terms.
        For each terms, store in a dictionary the documents in which the term appears (postings list).
        :return: list of postings lists found from the terms in the query.
        """
        results = {}

        for term in self.terms:
            try:
                results[term] = set(self.index[term])
            except KeyError:
                results[term] = set()

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
        print("%s: %s" % (self.__class__.__name__, " ".join(self.terms)))
        print("%s result(s) found: %s\n" % ("{:,}".format(len(results)), ", ".join(map(str, results)) if len(results) > 0 else "there are no results matching your query."))


class AndQuery(Query):

    def __init__(self, index, terms):
        Query.__init__(self, index, terms)

    def execute(self):
        """
        Get postings lists and conduct their intersection.
        :return: postings list for a query using conjunction (and).
        """
        postings_lists = self.get_postings_lists()
        results = sorted(postings_lists[0].intersection(*[postings_list for postings_list in postings_lists[1:]]))

        self.print_results(results)
        return results


class OrQuery(Query):

    def __init__(self, index, terms):
        Query.__init__(self, index, terms)

    def execute(self):
        """
        Get postings lists and conduct their union.
        :return: postings list for a query using disjunction (or).
        """
        postings_lists = self.get_postings_lists()
        results = sorted(postings_lists[0].union(*[postings_list for postings_list in postings_lists[1:]]))

        self.print_results(results)
        return results


def ask_user():
    query = input("Type in a search query.\n")
    print()
    return query
