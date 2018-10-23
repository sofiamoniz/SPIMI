#! /usr/bin/env python3
# coding: utf-8

import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

word_tokenize = word_tokenize
stopwords = set(stopwords.words("english"))
ps = PorterStemmer()
