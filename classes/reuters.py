#! /usr/bin/env python3
# coding: utf-8

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import os
import wget
import tarfile
from bs4 import BeautifulSoup

from definitions import ROOT_DIR


class Reuters:

    def __init__(self, docs_per_block=500, remove_stopwords=False, stem=False, case_folding=False, remove_numbers=False):
        """
        Initiate the Reuters objects which will contain the reuters files.
        :param docs_per_block: number of documents per generated block.
        :param remove_stopwords: will we include stopwords?
        :param stem: will we stem the terms?
        :param case_folding: will we lower terms to their lowercase variant?
        :param remove_numbers: will we remove terms that are just numbers?
        """
        self.reuters_url = "http://www.daviddlewis.com/resources/testcollections/reuters21578/reuters21578.tar.gz"
        self.reuters_directory = "/".join([ROOT_DIR, "reuters21578"])

        self.reuters_files = self.__init_reuters_files()[:1]

        self.docs_per_block = docs_per_block

        self.remove_stopwords = remove_stopwords
        self.stem = stem
        self.case_folding = case_folding
        self.remove_numbers = remove_numbers

        self.will_compress = self.remove_stopwords or self.stem or self.case_folding or self.remove_numbers

        if self.remove_stopwords:
            self.stopwords = set(stopwords.words("english"))

        if self.stem:
            self.ps = PorterStemmer()

        self.list_of_lists_of_tokens = []

    def get_reuters(self):
        """
        Download tar file and store in root directory of project.
        Extract contents into 'reuters21578' directory.
        Delete tar file.
        """
        if not os.path.exists(self.reuters_directory):
            print("Downloading Reuters files...")
            file = wget.download(self.reuters_url, ROOT_DIR)
            print()
            tar = tarfile.open(file)
            tar.extractall(path=self.reuters_directory)
            tar.close()
            os.remove(file)

    def __init_reuters_files(self):
        """
        First, get the reuters files from online.
        Then, grab the files in the reuters directory that end in with the .sgm file extension.
        :return: sorted list of reuters files ending with .sgm.
        """
        self.get_reuters()
        reuters_files = [os.path.join(self.reuters_directory, file)
                         for file in os.listdir(self.reuters_directory)
                         if file.endswith(".sgm")]

        return sorted(reuters_files)

    def get_tokens(self):
        """
        Find all tokens in the reuters files (self.reuters_files).
        For each file:
            - Find all REUTERS tags, each representing a document.
            - For each document, get its document ID (NEWID attribute).
            - If BODY tag is present, get tuples of (term, document ID) from its text, which represent tokens.

        :return: list of lists of tokens (tuples of (term, postings list)). Yes, list of lists of. It's a list of lists.
        Each list in the list represents a block that will be generated.
        """
        tokens = []
        current_document = 0
        number_of_documents = 0
        number_of_tokens = 0
        print("Parsing Reuters files...")

        for file in self.reuters_files:
            """
            We will use ISO-8859-1 encoding, because reut2-017.sgm is yielding a UnicodeDecodeError.
            We could always just put the 'errors' parameter to 'ignore' in the open() method.
            But after running a diff command, the only difference is the presence if a 'ü' character. We'll include it.
            """
            soup = BeautifulSoup(open(file, encoding="ISO-8859-1"), "html.parser")
            documents = soup.find_all("reuters")

            for document in documents:
                document_id = int(document['newid'])

                if document.body:
                    body = document.body.text
                    terms = word_tokenize(body)
                    if self.will_compress:
                        terms = self.compress(terms)
                    token_pairs = [(term, document_id) for term in terms]
                    tokens.extend(token_pairs)
                    number_of_documents += 1

                    current_document += 1
                    if current_document == self.docs_per_block:
                        number_of_tokens += len(tokens)
                        self.list_of_lists_of_tokens.append(tokens)
                        tokens = []
                        current_document = 0

        if tokens:
            number_of_tokens += len(tokens)
            self.list_of_lists_of_tokens.append(tokens)

        print("Found %s documents with bodies and %s tokens." % ("{:,}".format(number_of_documents), "{:,}".format(number_of_tokens)))
        return self.list_of_lists_of_tokens

    def compress(self, terms):
        """
        Remove stopwords from terms list, or stem terms in terms list, or lower terms to their lowercase variant, or
        remove terms that are just numbers.
        Or do any combination of all.
        :param terms: list of terms to be compressed.
        :return: compressed list of terms.
        """
        if self.remove_stopwords:
            terms = [term for term in terms if term.lower() not in self.stopwords]
        if self.stem:
            terms = [self.ps.stem(term) for term in terms]
        if self.case_folding:
            terms = [term.casefold() for term in terms]
        if self.remove_numbers:
            terms = [term for term in terms if not term.replace(",", "").replace(".", "").isdigit()]

        return terms
