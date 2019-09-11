# External Libraries used
# BeautifulSoup

import os
from bs4 import BeautifulSoup
from os import listdir
from string import punctuation
import re

def parse():
    directory= os.getcwd()
    filedirectory= directory+ "/" + "Documents"
    flist=(listdir(filedirectory))

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, 'transformed_corpus')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    print("1. Case Folding \n 2. No case folding")
    s1 = input()

    print("1. Remove punctuations \n 2. Keep punctuations")
    s2 = input()

    for file in flist:
        fname = filedirectory + "/" + file
        f=open(fname, "r")
        text = f.read()
        soup=BeautifulSoup(text, "xml")
        fs= ""
        for item in soup(["p"]):
            s = item.extract()
            fs = fs + s.get_text()

        lines = (line.strip() for line in fs.splitlines())
        # remove space on each line
        linebreakchunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # get chunks of newlines
        text = '\n'.join(linebreakchunk for linebreakchunk in linebreakchunks if linebreakchunk)
        # remove blanklines

        if s1 == '1':
            text = text.lower()

        text2 = ""

        if s2 == '1':

            for word in text.split():

                if word.find("[") == -1:
                    text2= text2 + ""
                elif bool(re.search(r'\d', word)) or word.find("-") != -1:
                    text2 = text2 + " " + word + " "
                else:
                    text2= text2 + " "
                    for c in word:
                        if c not in punctuation:
                            text2 = text2 + c
                        else:
                            text2 = text2 + " "

        x = final_directory + "/" + file
        y = open(x, "w")
        if s2 != 1:
            y.write(text)
        else:
            y.write(text2)

parse()


