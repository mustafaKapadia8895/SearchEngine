import os
from bs4 import BeautifulSoup
from os import listdir
from string import punctuation
import re

def clean():

    file = "cacm.query.txt"
    f=open(file, "r")
    t=f.read()

    soup = BeautifulSoup(t, "lxml")

    fs=""

    for item in soup.find_all("doc"):
        s=item.extract()
        for c in s.get_text():
            if c == "\n":
                fs=fs+ " "
            else:
                fs = fs + c
        fs=fs+"\n"

    fs=fs.lower()

    # citation : https://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
    # Beautify document by creating chunks, removing javascript, new lines and extra spaces
    lines = (line.strip() for line in fs.splitlines())
    # remove space on each line
    linebreakchunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # get chunks of newlines
    text = '\n'.join(linebreakchunk for linebreakchunk in linebreakchunks if linebreakchunk)
    # remove blanklines

    data = text


    # handling the punctuations
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

    f=open("transformed_queries.txt", "w")
    f.write(data)
    f.close()


    print(data)

clean()