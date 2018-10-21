# COMP 479 - Project 1

This is a project done for the fall 2018 COMP 479 - Information Retrieval course in Concordia University. The goal of the project was to analyze Reuters documents from a bunch of files by tokenizing the documents, subsequently constructing an index containing terms and their corresponding postings lists.

The Reuters files can be downloaded [here](http://www.daviddlewis.com/resources/testcollections/reuters21578/), though the program will download them for you once run (if they're not already available in the root directory of the project).

## Getting Started

### Prerequisites

The following Python packages are required to run the program:

- [nltk](https://pypi.org/project/nltk/)
- [bs4](https://pypi.org/project/beautifulsoup4/)

### Running

`python3 main.py [-mb MAX_BLOCK_SIZE] [-rs] [-s] [-c] [-rn]`

The arguments are the following:

1. `-mb` or `--max-block-size`: the max size of a block file, in megabytes.
2. `-rs` or `--remove-stopwords`: stopwords will be removed from index.
3. `-s` or `--stem`: terms in index will be stemmed.
4. `-c` or `--case-folding`: terms in index will be converted to lowercase.
5. `-rn` or `--remove-numbers`: terms that are just numbers will be removed from index.

## Author

- **Vartan Benohanian** - *ID:* 27492049

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
