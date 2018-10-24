#! /usr/bin/env python3
# coding: utf-8

import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(os.path.realpath(THIS_DIR))

word_tokenize = word_tokenize
stopwords = set(stopwords.words("english"))
ps = PorterStemmer()
