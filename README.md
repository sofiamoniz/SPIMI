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

Build the Docker image by running `docker build -t comp479:project-2 .`. The `-t` is used to tag the image, you can tag it however you like.

To run the container:

1. Run `docker container run -dit --name spimi comp479:project-2`. This will start a container in the background (because of the `-d` or `--detach` option).
    - You can add the `--rm` option, which will delete the container once you `exit` out of the shell.
    - You can also name the container however you like; I named it spimi.
2. To get access to an interactive Bash terminal: `docker container exec -it spimi bash`. You can [run the program](#running) from there.

Another way to get access to the terminal is by running the `bash` command as you first run the container:

1. `docker container run -dit --name spimi comp479:project-2 bash`.
2. `docker container attach spimi` will give you access to the `bash` terminal. If you hadn't specified `bash` previously, it would give you access to the `python` console.

Another way is to just dismiss the detached mode and just run:

1. `docker container run -it --name spimi comp479:project-2 bash`
2. Once you `exit` out, the container will stop.
3. To restart it, run `docker container start spimi`.
4. To go back in the shell, do `docker container attach spimi` or `docker container exec -it spimi bash`.

There are so many ways to do this.

### Running

The file to run is in the `src/` directory.

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

Generated files will appear in the root directory of the repository.

## Author

- **Vartan Benohanian** - *ID:* 27492049

## Report

A project report showcasing a more detailed description of the SPIMI is available [here](Project%201%20Report.pdf).

The one showcasing the Okapi BM ranking function can be viewed [here](Project%202%20Report.pdf).

The Expectations of Originality form is available [here](Expectations%20of%20Originality.pdf).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
