import os
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


this_directory = os.path.dirname(os.path.realpath(__file__))
reuters_directory = this_directory + "/reuters21578"
reuters_extension = ".sgm"
reuters_files = []
tokens = []


def get_reuters_files():
    for file in os.listdir(reuters_directory):
        if file.endswith(reuters_extension):
            reuters_files.append(os.path.join(reuters_directory, file))

    return sorted(reuters_files)


def get_tokens(files):
    documents_without_body = 0

    for file in files:
        with open(file) as file_to_read:
            data = file_to_read.read()

        soup = BeautifulSoup(data, "html.parser")
        documents = soup.find_all("reuters")                                # find all <REUTERS>...</REUTERS>
        print("Found %d documents." % len(documents))                       # number of <REUTERS>...</REUTERS>

        for document in documents:
            document_id = int(document['newid'])                            # NEWID attribute of REUTERS tag

            if document.body:                                               # is there a BODY tag in REUTERS?
                body = document.body.text                                   # BODY tag in REUTERS
                terms = word_tokenize(body)
                token_pairs = [(term, document_id) for term in terms]       # tuples containing (term, document_id)
                tokens.extend(token_pairs)
            else:
                documents_without_body += 1

    print("There are %d documents without a body." % documents_without_body)
    print("There are %d tokens." % len(tokens))
    return tokens


if __name__ == '__main__':
    get_tokens(get_reuters_files())
