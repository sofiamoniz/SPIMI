# Single-Pass In-Memory Indexing

This repository was made public on October 23, 2018.

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

1. Run `docker build -t comp479:project-1 .`.
    - The `-t` is used to tag the image, you can tag it however you like.
2. Run `docker container run -dit --name project comp479:project-1`. This will take you to an interactive terminal, where you'll be able to [run the program](#running).
    - You can add the `--rm` option, which will delete the container once you `exit` out of the shell.
    - You can also name the container however you like; I named it project.
3. To get access to an interactive Bash terminal: `docker container exec -it project bash`.

Another way to get access to the terminal is by running the `bash` command as you first run the container:

1. `docker container run -dit --name project comp479:project-1 bash`
2. `docker container attach project`, which gives you access to the `bash` terminal. If you hadn't specified `bash` previously, it would give you access to the `python` console.

Another way is to just let go of the detached mode and just run:

1. `docker container run -it --name project comp479:project-1 bash`
2. Once you `exit` out, the container will stop.
3. To restart it, do `docker container start project`.
4. To go back in the shell, do `docker container attach project` or `docker container exec -it project bash`.

There are so many ways to do this.

### Running

```
python3 main.py [-d DOCS_PER_BLOCK]
                [-r {1, 2, 3, ..., 22}]
                [-rs] [-s] [-c] [-rn]
                [-a]
```

The arguments are the following:

1. `-d` or `--docs`: number of documents per block. Default is 500.
2. `-r` or `--reuters`: number of Reuters files to parse, choice from 1 to 22. Default is 22.
3. `-rs` or `--remove-stopwords`: stopwords will be removed from index. Default is false.
4. `-s` or `--stem`: terms in index will be stemmed. Default is false.
5. `-c` or `--case-folding`: terms in index will be converted to lowercase. Default is false.
6. `-rn` or `--remove-numbers`: terms that are just numbers will be removed from index. Default is false.
7. `-a` or `--all`: includes options 3 to 6. Default is false.

## Author

- **Vartan Benohanian** - *ID:* 27492049

## Report

A project report showcasing a more detailed description of the project is available [here](Project%20Report.pdf).

The Expectations of Originality form is available [here](Expectations%20of%20Originality.pdf).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
