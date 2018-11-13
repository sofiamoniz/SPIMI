#! /usr/bin/env python3
# coding: utf-8

import os

from definitions import ROOT_DIR


class SPIMI:

    def __init__(self, reuters):
        """
        Initialize the SPIMI inverter with a list of tokens.
        :param reuters: Reuters object which will contain reuters files and methods to obtain tokens.
        """
        self.reuters = reuters

        self.output_directory = "DISK"
        self.output_directory = "/".join([ROOT_DIR, self.output_directory])

        self.block_prefix = "BLOCK"
        self.block_number = 0
        self.block_suffix = ".txt"

        self.output_index = "index"
        self.output_index = "/".join([self.output_directory, self.output_index + self.block_suffix])
        self.mkdir_output_directory(self.output_directory)

        self.list_of_lists_of_tokens = self.reuters.get_tokens()

    @staticmethod
    def mkdir_output_directory(output_directory):
        """
        Make an output directory in which we will store disk blocks.
        If it already exists, ask user if we should overwrite it.
        :param output_directory: directory in which output files will be generated.
        """
        try:
            os.mkdir(output_directory)
        except FileExistsError:
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
    def write_block_to_output_directory(sorted_terms, dictionary, block_file):
        """
        Create BLOCK*.txt file(s) in the output directory.
        The text file(s) will contain terms, with the document IDs in which they appear.
        :param terms: list of sorted terms.
        :param dictionary: dictionary containing terms as keys, and their corresponding list of postings as values.
        :param block_file: file in which data will be written.
        :return:
        """
        with open(block_file, 'w') as file:
            for term in sorted_terms:
                line = "%s %s\n" % (term, ' '.join([str(document_id) for document_id in dictionary[term]]))
                file.write(line)
        return block_file

    def construct_index(self):
        """
        Run the single-pass in-memory indexing (SPIMI) inversion algorithm.
        We start off with an empty dictionary.

        For each list of tokens in the list of lists of tokens, generate a dictionary, which will be dumpled into a
        block file.

        At the end of the method, the block files are used to construct the final inverted index.

        :return: a method call to merge the generated block files.
        """
        if os.path.exists(self.output_index):
            return self.get_index()

        block_files = []

        for list_of_tokens in self.list_of_lists_of_tokens:
            dictionary = {}

            for token in list_of_tokens:

                if token[0] not in dictionary:
                    postings_list = self.add_to_dictionary(dictionary, token[0])
                else:
                    postings_list = self.get_postings_list(dictionary, token[0])

                self.add_to_postings_list(postings_list, token[1])

            self.block_number += 1
            terms = self.sort_terms(dictionary)

            block_file = "/".join([self.output_directory, "".join([self.block_prefix, str(self.block_number), self.block_suffix])])
            block_files.append(self.write_block_to_output_directory(terms, dictionary, block_file))

        return self.merge_blocks(block_files)

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
              We do this by finding the minimum value in the list.
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
        :return: a method call to create a dictionary object from the merged index.
        """
        block_files = [open(block_file) for block_file in block_files]
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

                min_index = lines.index(min(lines))
                line = lines[min_index]
                current_term = line.split()[0]
                current_postings = " ".join(map(str, sorted(list(map(int, line.split()[1:])))))

                if current_term != most_recent_term:
                    output_index.write("\n%s %s" % (current_term, current_postings))
                    most_recent_term = current_term
                else:
                    output_index.write(" %s" % current_postings)

                lines[min_index] = block_files[min_index].readline()[:-1]

                if lines[min_index] == "":
                    block_files[min_index].close()
                    block_files.pop(min_index)
                    lines.pop(min_index)

            output_index.close()

        return self.get_index()

    def get_index(self):
        """
        This method will read the index file and create a dictionary object from it, containing terms as keys and their
        corresponding postings as values.

        We first initialize an empty dictionary, which will be the inverted index.
        Then we open the index file and return a stream. We read the first line since it's just a newline generated in
        the file from the merge_blocks() method.

        For every line of the index file:
        - We split it, using a space (" ") as the delimiter (default).
        - The first value in the list is the term (-> key).
        - The rest of the values in the list are the postings (-> value).
            • We make sure to make the postings are sorted.

        :return: the inverted index, i.e. the dictionary containing terms as keys, and a set of postings as values.
        """
        inverted_index = {}

        index_file = open(self.output_index)
        index_file.readline()

        for line in index_file:
            line = line.split()
            inverted_index[line[0]] = sorted(map(int, (line[1:])))

        return inverted_index
