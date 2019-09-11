import os
from os import listdir

def indexer():
    directory = os.getcwd()
    filedirectory = directory + "/" + "transformed_corpus"
    flist = (listdir(filedirectory))
    index={}
    word_count={}
    print("1. Unigrams\n2. Bigrams\n3. Trigrams")
    n=input()

    if n=='1':
        unidocfreq={}
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
                    # creae entry for word
                    file_index.update({word: 1})


            for key in file_index.keys():
                # check if word already exists in index
                if key in index:
                    # Append the file docID and word count to the word entry
                    index[key].append({file[:-4]: file_index[key]})
                    unidocfreq[key].append(file[:-4])

                else:
                    # Create an entry for the word
                    index.update({key: [{file[:-4]: file_index[key]}]})
                    unidocfreq.update({key: [file[:-4]]})

                if key in word_count.keys():
                    word_count[key] = word_count[key]+ file_index[key]
                else:
                    word_count.update({key: file_index[key]})
		
        # sort and save the indexes to files
        i=1
        x=open("uniword_count.txt", "w")
        for k in sorted(word_count, key=lambda  k: word_count[k], reverse=True):
            x.write(str(i)+"\t"+str(k) + "\t" + str(word_count[k]) + "\n")
            i+=1

        i = 1
        f = open("uniindex.txt", "w")
        for k in sorted(word_count, key=lambda  k: word_count[k], reverse=True):
            f.write(str(i) + "\t" + str(k) + "\t" + str(index[k]) + "\n\n\n\n")
            i += 1

        f=open("unidocfreq", "w")
        for k in sorted(unidocfreq):
            f.write(str(k) + "\t" + str(unidocfreq[k]) + "\t"+ str(len(unidocfreq[k]))+ "\n")


    if n=='2':
        bidocfreq={}
        for file in flist:
            fname = filedirectory + "/" + file
            f = open(fname, "r")
            text = f.read()
            file_index = {}

            x=0
            l=text.split()
            while x< len(l)-1:
                word= l[x]+ " " + l[x+1]
                if word in file_index.keys():
                    file_index[word] += 1

                else:
                    file_index.update({word: 1})

                x += 1

            for key in file_index.keys():
                if key in index:
                    index[key].append({file[:-4]: file_index[key]})
                    bidocfreq[key].append(file[:-4])

                else:
                    index.update({key: [{file[:-4]: file_index[key]}]})
                    bidocfreq.update({key: [file[:-4]]})


                if key in word_count.keys():
                    word_count[key] = word_count[key] + file_index[key]
                else:
                    word_count.update({key: file_index[key]})


        i=1
        x = open("biword_count.txt", "w")
        for k in sorted(word_count, key=lambda k: word_count[k], reverse=True):
            x.write(str(i)+"\t"+str(k) + "\t" + str(word_count[k]) + "\n")
            i+=1

        i = 1
        f = open("biindex.txt", "w")
        for k in sorted(word_count, key=lambda k: word_count[k], reverse=True):
            f.write(str(i) + "\t" + str(k) + "\t" + str(index[k]) + "\n\n\n\n")
            i += 1

        f = open("bidocfreq", "w")
        for k in sorted(bidocfreq):
            f.write(str(k) + "\t" + str(bidocfreq[k]) + "\t" + str(len(bidocfreq[k])) + "\n")


    if n=='3':
        tridocfreq={}
        for file in flist:
            fname = filedirectory + "/" + file
            f = open(fname, "r")
            text = f.read()
            file_index = {}

            x=0
            l=text.split()
            while x< len(l)-2:
                word= l[x]+ " " + l[x+1] + " " + l[x+2]
                if word in file_index.keys():
                    file_index[word] += 1

                else:
                    file_index.update({word: 1})

                x += 1

            for key in file_index.keys():
                if key in index:
                    index[key].append({file[:-4]: file_index[key]})
                    tridocfreq[key].append(file[:-4])

                else:
                    index.update({key: [{file[:-4]: file_index[key]}]})
                    tridocfreq.update({key: [file[:-4]]})

                if key in word_count.keys():
                    word_count[key] = word_count[key] + file_index[key]
                else:
                    word_count.update({key: file_index[key]})


        i=1
        x = open("triword_count.txt", "w")
        for k in sorted(word_count, key=lambda k: word_count[k], reverse=True):
            x.write(str(i)+"\t"+str(k) + "\t" + str(word_count[k]) + "\n")
            i+=1

        i = 1
        f = open("triindex.txt", "w")
        for k in sorted(word_count, key=lambda k: word_count[k], reverse=True):
            f.write(str(i) + "\t" + str(k) + "\t" + str(index[k]) + "\n\n\n\n")
            i += 1

        f = open("tridocfreq", "w")
        for k in sorted(tridocfreq):
            f.write(str(k) + "\t" + str(tridocfreq[k]) + "\t" + str(len(tridocfreq[k])) + "\n")






indexer()