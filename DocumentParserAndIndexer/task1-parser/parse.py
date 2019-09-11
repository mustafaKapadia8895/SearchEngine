# External Libraries used
# BeautifulSoup
# citation
# https://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript

import os
from bs4 import BeautifulSoup
from os import listdir
from string import punctuation
import re

def parse():
    # Retrieve file names from corpus
    directory= os.getcwd()
    filedirectory= directory+ "/" + "Documents"
    flist=(listdir(filedirectory))

    # Create directory for transformed documents
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
        for item in soup(["title"]):
            s = item.extract()

            fs = fs + s.get_text()

        # citation : https://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
        # Beautify document by creating chunks, removing javascript, new lines and extra spaces
        lines = (line.strip() for line in fs.splitlines())
        # remove space on each line
        linebreakchunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # get chunks of newlines
        text = '\n'.join(linebreakchunk for linebreakchunk in linebreakchunks if linebreakchunk)
        # remove blanklines

        if s1 == '1':
            text = text.lower()

        data=text

        if s2 == '1':

            remove_punc = re.compile('[\.,;!@#$%^&:\(\)\?"\']')
            remove_ref = re.compile('\[.*?\]')
            remove_style = re.compile('{.*}')

            p = re.compile('(\d+)\.(\d+)')
            data = p.sub(r'\1*\2', data)

            data = re.sub(remove_ref, '', data)
            data = re.sub(remove_punc, '', data)

            replace_dots = re.compile('\*')
            data = re.sub(replace_dots, '.', data)
            data = re.sub(remove_style, '', data)


            # for word in text.split():
            #
            #     if word.find("[") != -1:
            #         text2= text2 + ""
            #     # Check if word is a number or contains a hyphen
            #     elif bool(re.search(r'\d', word)) or word.find("-") != -1:
            #         text2 = text2 + " " + word + " "
            #     # Remove punctuations
            #     else:
            #         text2= text2 + " "
            #         for c in word:
            #             if c not in punctuation:
            #                 text2 = text2 + c
            #             else:
            #                 text2 = text2 + " "





        # save transformed documents to file
        x = final_directory + "/" + file
        y = open(x, "w")
        if s2 != '1':
            y.write(text)
        else:
            y.write(data)

parse()


