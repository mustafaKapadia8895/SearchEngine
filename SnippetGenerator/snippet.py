import os
from os  import listdir
from os.path import isfile, join


def snippet():

    f=open("common_words.txt", "r")
    text=f.read()
    stop= text.split("\n")

    window_size=20
    current_directory = os.getcwd()
    path = os.path.join(current_directory, 'QueryResults')

    directory = os.getcwd()
    filedirectory = directory + "/" + "transformed_corpus"

    f=open("transformed_queries.txt")

    q=1
    for query in f.read().split("\n"):

        outputfile = "Q" + str(q) + "results.html"
        outputfile = os.path.join(directory, "Results", outputfile)
        print(outputfile)
        if not os.path.exists(os.path.dirname(outputfile)):
            os.makedirs(os.path.dirname(outputfile))


        temp = query.split()
        temp = "Q" + temp[0]

        fname = path + "/BM25 - "+temp+".txt"
        tempf = open(fname, "r")
        data = tempf.read()
        data = data.splitlines()
        querytop100resultlist = []
        for lines in data:
            words = lines.split()
            querytop100resultlist += [words[2]]

        qlist = query.split()
        qlist=qlist[1:]

        for name in querytop100resultlist:

                final= filedirectory+"/"+name

                f=open(final, "r")
                text=f.read()
                tlist=text.split()
                tlist=tlist[2:-2]

                k=-1
                i=0
                max = -1

                while i<len(tlist)+window_size:
                    count=0

                    for word in tlist[i:i+window_size]:
                        if word in qlist and word not in stop:
                            count+=1

                    if count > max:
                        max=count
                        k=i

                    i+=1


                snippet=""
                i=0
                while i<window_size and i+k< len(tlist):
                    if tlist[k+i] in qlist and tlist[k+i] not in stop:
                        snippet+= "<mark><b>"+tlist[k+i]+"</b></mark>"+ " "
                    else:
                        snippet+=tlist[k+i]+" "
                    i+=1

                f=open(outputfile, "a")

                f.write(name+"<br>..."+snippet+"...<br><br><br>")

        q+=1


snippet()

