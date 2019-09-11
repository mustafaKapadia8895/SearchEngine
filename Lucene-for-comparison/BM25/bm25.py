import os
from os import listdir
import math

def bm25():
    directory = os.getcwd()
    filedirectory = directory + "/" + "transformed_corpus"

    flist = (listdir(filedirectory))

    # Compute index
    index=make_index()

    f=open("queries.txt", "r")
    q=f.read()
    queries=q.split("\n")

    # Initialize required variables
    k1=1.2
    k2=100
    b=0.75
    avdl=0
    dl=[]
    K=[]
    N= len(flist)

    # Compute document lengths
    for file in flist:
        fname = filedirectory + "/" + file
        f = open(fname, "r")
        text = f.read()
        dl.append(len(text))
        avdl+= len(text)

    #Compute average document length
    avdl = avdl / len(flist)

    # Compute K for each document
    i=0
    for item in dl:
        temp = (k1 * (1-b)) + (b * dl[i]/ avdl)
        K.append(temp)
        i+=1

    q=1
    for query in queries:
        i = 0
        scores = {}
        for file in flist:

            terms = query.split(" ")
            score = 0

            for term in terms:
                ni=len(index[term])
                l= index[term]
                fi=0
                for entry in l:
                    if file[:-4] in entry:
                        fi= entry[file[:-4]]

                # For every query term in every query compute score for every document
                if fi!=0:
                    first = 1/ (ni+0.5)* (N-ni+0.5)
                    second= (k1+1)* fi / (K[i]+fi)
                    third = (k2+1)* terms.count(term)/(k2+ terms.count(term))
                    score+= math.log(first) * second * third

            # Handle documents containing no query terms
            if score==0:
                scores.update({file : -999})
            else:
                scores.update({file : score})
            i += 1

        # rank the documents by score
        rank(scores, q)
        q+=1


def rank(scores, q):
    i=1

    if(i==1):
        f = open("scores"+ str(q)+".txt", "w")
    else:
        f=open("scores"+ str(q)+".txt", "a")

    # save scores to file
    for k in sorted(scores, key=lambda  k: scores[k], reverse=True):
            f.write(str(q)+"\tQ0\t"+str(k) + "\t"+ str(i)+ "\t" + str(scores[k]) + "\tBM25CaseFoldPuncRem\n")
            i+=1
            if i==101:
                break

def make_index():
    directory = os.getcwd()
    filedirectory = directory + "/" + "transformed_corpus"
    flist = (listdir(filedirectory))
    index={}
    word_count = {}
    for file in flist:
        fname = filedirectory + "/" + file
        f=open(fname, "r")
        text = f.read()
        file_index={}

        for word in text.split():
            # check if word exists in index
            if word in file_index.keys():
                # increase word count
                file_index[word] += 1

            else:
                # create entry for word
                file_index.update({word: 1})


        for key in file_index.keys():
            # check if word already exists in index
            if key in index:
                # Append the file docID and word count to the word entry
                index[key].append({file[:-4]: file_index[key]})
            else:
                # Create an entry for the word
                index.update({key: [{file[:-4]: file_index[key]}]})

            if key in word_count.keys():
                word_count[key] = word_count[key] + file_index[key]
            else:
                word_count.update({key: file_index[key]})

    i=0
    f = open("uniindex.txt", "w")
    for k in sorted(word_count, key=lambda k: word_count[k], reverse=True):
        f.write(str(i) + "\t" + str(k) + "\t" + str(index[k]) + "\n\n\n\n")
        i += 1
    return index

bm25()