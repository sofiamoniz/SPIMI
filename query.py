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
        return


class AndQuery(Query):

    def __init__(self, index, words):
        Query.__init__(self, index, words)

    def execute(self):
        postings_lists = self.get_postings_lists()
        result = sorted(postings_lists[0].intersection(*[postings_list for postings_list in postings_lists[1:]]))

        print("%d result(s) found: %s" % (len(result), ", ".join(map(str, result))))
        return result


class OrQuery(Query):

    def __init__(self, index, words):
        Query.__init__(self, index, words)

    def execute(self):
        postings_lists = self.get_postings_lists()
        result = sorted(postings_lists[0].union(*[postings_list for postings_list in postings_lists[1:]]))

        print("%d result(s) found: %s" % (len(result), ", ".join(map(str, result))))
        return result
