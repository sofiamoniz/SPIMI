#! /usr/bin/env python3
# coding: utf-8

import sys
import os
from definitions import ROOT_DIR


class SPIMI:

    def __init__(self, tokens, output_directory="DISK", block_size_limit=1):
        """
        Initiate the SPIMI inverted with a list of tokens and a block size limit.
        :param tokens: list of tuples containing a term and a document ID.
        :param block_size_limit: maximum size of a block, in megabytes. Default is 1.
        """
        self.it_tokens = iter(tokens)
        self.output_prefix = "BLOCK"
        self.output_suffix = ".txt"
        self.output_directory = "%s/%s/" % (ROOT_DIR, output_directory)
        self.block_size_limit = block_size_limit
        self.block_number = 0

        self.mkdir_output_directory(self.output_directory)

    @staticmethod
    def mkdir_output_directory(output_directory):
        """
        Make an output directory in which we will store disk blocks.
        If it already exists, ask user if we should overwrite it.
        :param output_directory: directory in which output files will be generated.
        :return: True if directory is created, else False.
        """
        try:
            os.mkdir(output_directory)
            print("%s directory created." % output_directory)
            return True
        except FileExistsError:
            print("%s directory already exists. Erasing its contents..." % output_directory)
            for file in os.listdir(output_directory):
                os.unlink(os.path.join(output_directory, file))

    @staticmethod
    def add_to_dictionary(dictionary, term):
        """
        Add a new term (key) to the dictionary.
        :param dictionary: dictionary containing terms as keys, and their corresponding list of postings as values.
        :param term: new term that we will add.
        :return: newly updated dictionary containing the new term, with an empty list as its value.
        """
        dictionary[term] = []
        return dictionary[term]

    @staticmethod
    def get_postings_list(dictionary, term):
        """
        Get list of postings of the term.
        :param dictionary: dictionary containing terms as keys, and their corresponding list of postings as values.
        :param term: term (key in dictionary) we are looking for.
        :return: term's list of postings.
        """
        return dictionary[term]

    @staticmethod
    def add_to_postings_list(postings_list, document_id):
        """
        Add document ID to term's postings list.
        :param postings_list: list of postings of the term.
        :param document_id: document in which term appears.
        """
        postings_list.append(document_id)

    @staticmethod
    def sort_terms(dictionary):
        """
        Get terms (keys) from dictionary and sort them alphabetically.
        :param dictionary: dictionary containing terms as keys, and their corresponding list of postings as values.
        :return: list of alphabetically sorted terms.
        """
        return [term for term in sorted(dictionary)]

    @staticmethod
    def write_block_to_output_directory(terms, dictionary, output_file):
        """
        Create BLOCK*.txt file(s) in the output directory.
        The text file(s) will contain terms, with the document IDs in which they appear.
        :param terms: list of SORTED terms.
        :param dictionary: dictionary containing terms as keys, and their corresponding list of postings as values.
        :param output_file:
        :return:
        """
        with open(output_file, 'w') as file:
            for term in terms:
                line = "%s %s\n" % (term, ' '.join([str(document_id) for document_id in dictionary[term]]))
                file.write(line)
        return output_file

    def create_inverted_index(self):
        """
        Run the single-pass in-memory indexing (SPIMI) inversion algorithm.
        We start off with an empty dictionary.

        As long as the size of the dictionary is less than the block_size_limit, we iterate through the tokens list and
        add them to the dictionary, along with their document IDs.

        If the dictionary gets too big, we dump its contents into a block file, and restart the process with a new empty
        dictionary, iterating through the rest of the list of tokens.

        :return: list of generated output files.
        """
        output_files = []
        iteration_complete = False

        while not iteration_complete:
            dictionary = {}
            try:
                while sys.getsizeof(dictionary) / 1024 / 1024 <= self.block_size_limit:
                    token = next(self.it_tokens)

                    if token[0] not in dictionary:
                        postings_list = self.add_to_dictionary(dictionary, token[0])
                    else:
                        postings_list = self.get_postings_list(dictionary, token[0])

                    self.add_to_postings_list(postings_list, token[1])
            except StopIteration:
                print("Done iterating through tokens. SPIMI inversion complete.\n")
                iteration_complete = True

            self.block_number += 1
            terms = self.sort_terms(dictionary)

            output_file = "%s%s%d%s" % (self.output_directory, self.output_prefix, self.block_number, self.output_suffix)
            output_files.append(self.write_block_to_output_directory(terms, dictionary, output_file))

        return output_files
