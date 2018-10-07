import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from get_reuters import get_reuters


this_directory = os.path.dirname(os.path.realpath(__file__))
reuters_directory = this_directory + "/reuters21578"
reuters_extension = ".sgm"
reuters_files = []
tokens = []


def get_reuters_files():
    get_reuters()

    for file in os.listdir(reuters_directory):
        if file.endswith(reuters_extension):
            reuters_files.append(os.path.join(reuters_directory, file))

    return sorted(reuters_files)


def get_tokens(files):
    for file in files:
        with open(file) as file_to_read:
            data = file_to_read.read()

        """
        Find all REUTERS tags.
        These represent the number of documents.
        """
        soup = BeautifulSoup(data, "html.parser")
        documents = soup.find_all("reuters")
        print("Found %d documents." % len(documents))

        for document in documents:
            # NEWID attribute of REUTERS tag
            document_id = int(document['newid'])

            """
            Is there a BODY tag in REUTERS?
            If so, get tuples of (term, document_id).
            """
            if document.body:
                body = document.body.text
                terms = word_tokenize(body)
                token_pairs = [(term, document_id) for term in terms]
                tokens.extend(token_pairs)

    print("There are %d tokens." % len(tokens))
    return tokens
