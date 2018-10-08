#! /usr/bin/env python3
# coding: utf-8

import sys
import os
from definitions import ROOT_DIR
from functools import reduce


class SPIMI:

    def __init__(self, tokens, output_directory="DISK", output_index="index", block_size_limit=1):
        """
        Initiate the SPIMI inverted with a list of tokens and a block size limit.
        :param tokens: list of tuples containing a term and a document ID.
        :param block_size_limit: maximum size of a block, in megabytes. Default is 1.
        """
        self.it_tokens = iter(tokens)
        self.output_prefix = "BLOCK"
        self.output_suffix = ".txt"
        self.output_directory = "/".join([ROOT_DIR, output_directory])
        self.output_index = "/".join([self.output_directory, output_index + self.output_suffix])
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
    def write_block_to_output_directory(terms, dictionary, block_file):
        """
        Create BLOCK*.txt file(s) in the output directory.
        The text file(s) will contain terms, with the document IDs in which they appear.
        :param terms: list of SORTED terms.
        :param dictionary: dictionary containing terms as keys, and their corresponding list of postings as values.
        :param block_file: file in which data will be written.
        :return:
        """
        with open(block_file, 'w') as file:
            for term in terms:
                line = "%s %s\n" % (term, ' '.join([str(document_id) for document_id in dictionary[term]]))
                file.write(line)
        return block_file

    def create_inverted_index(self):
        """
        Run the single-pass in-memory indexing (SPIMI) inversion algorithm.
        We start off with an empty dictionary.

        As long as the size of the dictionary is less than the block_size_limit, we iterate through the tokens list and
        add them to the dictionary, along with their document IDs.

        If the dictionary gets too big, we dump its contents into a block file, and restart the process with a new empty
        dictionary, iterating through the rest of the list of tokens.

        At the end of the method, the block files are used to create the final inverted index.
        """
        block_files = []
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
                print("Done iterating through tokens. SPIMI inversion complete.")
                iteration_complete = True

            self.block_number += 1
            terms = self.sort_terms(dictionary)

            block_file = "/".join([self.output_directory, "".join([self.output_prefix, str(self.block_number), self.output_suffix])])
            block_files.append(self.write_block_to_output_directory(terms, dictionary, block_file))

        if self.block_number == 1:
            print("%d block file has been generated." % self.block_number)
        else:
            print("%d block files have been generated." % self.block_number)

        self.merge_blocks(block_files)

    def merge_blocks(self, block_files):
        """
        Merging the block files.

        First, we initialize a list containing an open stream of all block files, which we will subsequently read.
        Next, we initialize a list containing the first line of each of those block files.
        NOTE: When we see a [:-1], it is used to delete the trailing newline in the string returned when reading a file.

        We keep a variable containing the most recent term also. At first, we initialize it to an empty string "".

        We run a check to ensure that each file isn't empty. When you read an empty file, you get returned an empty
        string "". We want to delete those files from the list from the beginning.

        Then, we open the index file, with write permissions.
        We run the following sequence as long as there are still block files to be read:
            - In the list of lines, we find the index of the one which comes first alphabetically, compared to the rest.
            - Using that, we compare the term in the line to the most recent term:
                • If they're not equal, we create a new line in the index with the new word, and its postings from the
                  current block file.
                • If they're equal, then since it's the most recent term, it's the most recent (last) line in the index
                  file currently. So we just extend the term's postings list by adding on to it in the index file.
            - After all of that, we replace the line we just used in the list of lines, with the next line of the block
              file. If there are no more lines to be read, we'd get an empty string "", in which case we'd close and
              delete the block file from the list of block files, as well as its line from the list of lines.
            - Once there are no more block files, we close the index file.

        :param block_files: list of block files which will be merged together to create an index file.
        """
        block_files = [open(block_file, "r") for block_file in block_files]
        lines = [block_file.readline()[:-1] for block_file in block_files]
        most_recent_term = ""

        index = 0
        for block_file in block_files:
            if lines[index] == "":
                block_files.pop(index)
                lines.pop(index)
            else:
                index += 1

        with open(self.output_index, "w") as output_index:
            while len(block_files) > 0:

                smallest_word_index = lines.index(reduce(lambda x, y: min(x, y), lines))
                line = lines[smallest_word_index]

                if line.split()[0] != most_recent_term:
                    output_index.write("\n%s" % line)
                    most_recent_term = line.split()[0]
                else:
                    output_index.write(" %s" % " ".join(line.split()[1:]))

                lines[smallest_word_index] = block_files[smallest_word_index].readline()[:-1]

                if lines[smallest_word_index] == "":
                    block_files[smallest_word_index].close()
                    block_files.pop(smallest_word_index)
                    lines.pop(smallest_word_index)

            output_index.close()

        print("Merge complete. The merged index can be found at %s.\n" % self.output_index)
