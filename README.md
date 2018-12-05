# Single-Pass In-Memory Indexing

This is a project done for the fall 2018 COMP 479 - Information Retrieval course in Concordia University. The goal of the project was to analyze Reuters documents from a bunch of files by tokenizing the documents, subsequently constructing an index containing terms and their corresponding postings lists.

The Reuters files can be downloaded [here](http://www.daviddlewis.com/resources/testcollections/reuters21578/), though the program will download them for you once run (if they're not already available in the root directory of the project).

## Getting Started

### Prerequisites

The following Python packages are required to run the program:

- [nltk](https://pypi.org/project/nltk/)
- [bs4](https://pypi.org/project/beautifulsoup4/)
- [wget](https://pypi.org/project/wget/)
- [beautifultable](https://pypi.org/project/beautifultable/)

Click [here](requirements.txt) for the specific versions of the packages used for this project.

Or just run it with [Docker](#docker).

### Docker

I also included a Dockerfile to make it easier to run on any machine. First, make sure you `cd` into this repository.

To build the image and start up a container:

```
docker image build -t spimi .
docker container run -it --name spimi-demo spimi bash
```

This will take you to an interactive Bash terminal, from which you can [run](#running) the script. You can include the `--rm` option in the `run` command to automatically remove the container when you exit out of it.

### Running

The file to run is in the `src/` directory.

```
python3 main.py [-d DOCS_PER_BLOCK]
                [-r {1, 2, 3, ..., 22}]
                [-rs] [-s] [-c] [-rn]
                [-a]

optional arguments:
    -d, --docs                      number of documents per block (default 500)
    -r, --reuters                   number of Reuters files to parse (1-22) (default 22)
    -rs, --remove-stopwords         remove stopwords from the index
    -s, --stem                      stem terms in the index
    -c, --case-folding              reduce terms in the index to lowercase
    -rn, --remove-numbers           remove numbers from the index
    -a, --all                       use options -rs, -s, -c, and -rn
```

Generated files will appear in the root directory of the repository.

## Author

- **Vartan Benohanian** - *ID:* 27492049

## Report

A project report showcasing a more detailed description of the SPIMI is available [here](Project%201%20Report.pdf).

The one showcasing the Okapi BM ranking function can be viewed [here](Project%202%20Report.pdf).

The Expectations of Originality form is available [here](Expectations%20of%20Originality.pdf).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
