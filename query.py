#! /usr/bin/env python3
# coding: utf-8

import abc


class Query:

    def __init__(self, index, words):
        self.index = index
        self.words = words

    def get_postings_lists(self):
        terms = self.words.split()
        results = {}

        for term in terms:
            try:
                results[term] = set(self.index[term])
            except KeyError:
                results[term] = set()

        return list(results.values())

    @abc.abstractmethod
    def execute(self):
        if self.__class__.__name__ == "Query":
            print("You are conducting a query using the %s class." % self.__class__.__name__)
            print("Make sure to use either AndQuery or OrQuery.\n")
        return

    def print_results(self, results):
        print("%s: %s" % (self.__class__.__name__, self.words))
        print("%d result(s) found: %s\n" % (len(results), ", ".join(map(str, results)) if len(results) > 0 else "there are no results matching your query."))


class AndQuery(Query):

    def __init__(self, index, words):
        Query.__init__(self, index, words)

    def execute(self):
        postings_lists = self.get_postings_lists()
        results = sorted(postings_lists[0].intersection(*[postings_list for postings_list in postings_lists[1:]]))

        self.print_results(results)
        return results


class OrQuery(Query):

    def __init__(self, index, words):
        Query.__init__(self, index, words)

    def execute(self):
        postings_lists = self.get_postings_lists()
        results = sorted(postings_lists[0].union(*[postings_list for postings_list in postings_lists[1:]]))

        self.print_results(results)
        return results
