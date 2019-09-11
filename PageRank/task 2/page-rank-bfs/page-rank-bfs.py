# External Libraries used
# BeautifulSoup

# Citations
# Video referred to for beautiful soup syntax-
# https://www.youtube.com/watch?v=3xQTJi2tqgk

# Code for saving contents of a list to a file-
# https://bbs.archlinux.org/viewtopic.php?id=75839

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import math


# Function for Crawling pages


def crawl(url):
    # Initializing required constants and variables
    base = 'https://en.wikipedia.org/wiki'
    max_depth = 6
    frontier = list()
    visited = list()
    content = list()
    docIds = list()
    frontier.append(url)
    flag = 0
    current_depth = 0
    first_url_of_next_depth = url
    while len(visited) < 1000 and frontier != [] and current_depth <= max_depth:
        next_url = frontier.pop(0)

        # Check to see if url has already been visited
        if next_url not in visited:

            # Check to see if depth has increased
            if next_url == first_url_of_next_depth:
                if current_depth != 0:
                    print("depth " + str(current_depth) + " crawled")
                current_depth = current_depth + 1
                print("crawling pages at depth:" + str(current_depth))
                flag = 1

            # Retrieve web page using beautiful soup
            time.sleep(1)
            r = requests.get(next_url)
            soup = BeautifulSoup(r.content)

            # Search for valid links within the page
            for link in soup.find_all("a"):
                parent = link.parent.name
                if parent == "p":
                    href = str(link.get("href"))
                    # Represent href in proper form using proper domain name
                    # Example /cyclone becomes https://en.wikipedia.org/wiki/cyclone
                    t = urljoin(base, href)

                    # Check if link already in frontier
                    if str(t) not in frontier:
                        # Check if link belongs to the same domain
                        if t.find(base) != -1:
                            # Check if the link points to contents on the same page
                            if t.find("#") == -1:
                                # If all false add link to frontier
                                frontier.append(str(t))
                                # if flag is set update first_url_of_next_depth
                                if flag == 1:
                                    first_url_of_next_depth = (str(t))
                                    flag = 0

            # Add crawled link to visited list
            visited.append(next_url)
            # Saving contents of visited page to content list
            soup.prettify()
            content.append(str(soup))
            j = next_url.find("wiki/")
            docId = str(next_url)[j + 5:]
            docIds.append(docId)

    print("maximum depth reached: " + str(current_depth))
    save_to_file(frontier, visited, content, docIds)
    construct_graph(visited, content, docIds)


# Code for saving contents of a list to a file-
# https://bbs.archlinux.org/viewtopic.php?id=75839


def save_to_file(frontier, visited, content, docIds):
    # Saving visited list to text file
    f = open("visited.txt", "w")
    f.write("\n".join(map(lambda x: str(x), visited)))
    f.close()

    # Saving frontier list to text file
    f = open("frontier.txt", "w")
    f.write("\n".join(map(lambda x: str(x), frontier)))
    f.close()

    # Saving contents list to file
    f = open("content.txt", "w")
    f.write("\n".join(map(lambda x: str(x), content)))
    f.close()

    # Saving titles list to file
    f = open("docIds.txt", "w")
    f.write("\n".join(map(lambda x: str(x), docIds)))
    f.close()


def construct_graph(visited, content, docIds):
    i = 0
    graph = list()
    graph2 = list()
    nooutlinks=list()
    outlinks=list()
    while i < len(visited):
        outlinks.append(0)

        j = 0
        s = docIds[i]
        p = ""
        while j < len(visited):
            if content[j].find("wiki/" + docIds[i]) != -1 and docIds[i] != docIds[j]:
                s = s + "\t" + docIds[j]
                if p == "":
                    p = p + str(j)
                else:
                    p = p + " " + str(j)
            j = j + 1
        i = i + 1
        graph.append(s)
        graph2.append(p)


    k = 0
    while k < len(graph2):
        for n in graph2[k].split(" "):
            outlinks[int(n)] += 1
        k += 1

    l = 0
    for n in outlinks:
        if n == 0:
            nooutlinks.append(l)

        l += 1

    save_graph_to_file(graph, graph2, outlinks, nooutlinks)
    page_rank(docIds, nooutlinks, graph2, outlinks, 0.85)


def save_graph_to_file(graph, graph2, outlinks, nooutlinks):
    # Saving graph list to file
    f = open("graph.txt", "w")
    f.write("\n".join(map(lambda x: str(x), graph)))
    f.close()

    # Saving graph2 list to file
    f = open("graph2.txt", "w")
    f.write("\n".join(map(lambda x: str(x), graph2)))
    f.close()

    f = open("outlinks.txt", "w")
    f.write("\n".join(map(lambda x: str(x), outlinks)))
    f.close()

    f = open("nooutlinks.txt", "w")
    f.write("\n".join(map(lambda x: str(x), nooutlinks)))
    f.close()

def page_rank(p, s, mp, lq, d):
    pr = list()
    newpr = list()
    perplexity=list()
    i = 0
    h=0
    perp=0
    n = len(p)
    while i < n:
        pr.append(1/n)
        newpr.append(1/n)
        i = i + 1
    x=0
    y=0
    while y < 4:
        h = convergence(pr)
        perpnew = pow(2, h)
        if perp-perpnew < 1:
            y += 1
        else:
            y=0
        perplexity.append(perpnew)
        perp=perpnew

        sinkpr = 0

        for j in s:
            sinkpr = sinkpr + pr[j]

        k = 0
        while k < n:

            newpr[k] = (1-d)/n
            newpr[k] = newpr[k] + (d * (sinkpr/n))
            for q in mp[k].split(" "):
                newpr[k] = newpr[k] + (d * pr[int(q)] / lq[int(q)])

            k=k+1

        l = 0
        while l < n:
            pr[l] = newpr[l]
            l = l+1
        x = x+1
    put_in_file(p, pr , perplexity)



def convergence(pr):
    i = 0
    h=0
    while i < len(pr):
        h = h + (pr[i] * math.log(pr[i], 2))
        i += 1

    return -h



def put_in_file(p, pr, perplexity):
    f = open("ranks.txt", "w")
    f.write("\n".join(reversed(sorted(map(lambda x, y: str(x) + "\t" + y, pr, p)))))
    f.close()

    f = open("perplexities.txt", "w")
    f.write("\n".join(map(lambda x: str(x), perplexity)))
    f.close()



crawl("https://en.wikipedia.org/wiki/Tropical_cyclone")