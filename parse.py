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

    for file in files:
        soup = BeautifulSoup(open(file), "html.parser")
        documents = soup.find_all("reuters")
        print("Found %d documents." % len(documents))

        for document in documents:
            document_id = int(document['newid'])

            if document.body:
                body = document.body.text
                terms = word_tokenize(body)
                token_pairs = [(term, document_id) for term in terms]
                tokens.extend(token_pairs)

    print("There are %d tokens." % len(tokens))
    return tokens
