#! /usr/bin/env python3
# coding: utf-8

from get_reuters import *
from parse import *
from spimi_invert import *


if __name__ == '__main__':
    if not SpimiInvert.mkdir_disk():
        print("Terminating program.")
    else:
        reuters_files = get_reuters_files()
        tokens = get_tokens(reuters_files)
        spimi = SpimiInvert(tokens)
        print(spimi.run())
