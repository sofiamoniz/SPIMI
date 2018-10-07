#! /usr/bin/env python3
# coding: utf-8

from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


def get_tokens(files):
    """
    Find all tokens in the reuters files.
    For each file:
        - Find all REUTERS tags, each representing a document.
        - For each document, get its document ID (NEWID attribute).
        - If BODY tag is present, get tuples of (term, document ID) from its text, which represent tokens.

    :param files: reuters files
    :return: list of tokens
    """
    tokens = []
    number_of_documents = 0
    print("Parsing Reuters files...")

    for file in files:
        """
        We will use ISO-8859-1 encoding, because reut2-017.sgm is yielding a UnicodeDecodeError.
        We could always just put the 'errors' parameter to 'ignore' in the open() method.
        But after running a diff command, the only difference is the presence if a 'ü' character. Why not include it?
        """
        soup = BeautifulSoup(open(file, encoding="ISO-8859-1"), "html.parser")
        documents = soup.find_all("reuters")
        number_of_documents += len(documents)

        for document in documents:
            document_id = int(document['newid'])

            if document.body:
                body = document.body.text
                terms = word_tokenize(body)
                token_pairs = [(term, document_id) for term in terms]
                tokens.extend(token_pairs)

    print("Found %s documents and %s tokens." % ("{:,}".format(number_of_documents), "{:,}".format(len(tokens))))
    return tokens
