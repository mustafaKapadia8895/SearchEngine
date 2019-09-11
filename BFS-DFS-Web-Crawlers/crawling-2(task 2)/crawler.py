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

# Function for Crawling pages


def crawl(url, keyword):
    # Initializing required constants and variables
    base = 'https://en.wikipedia.org/wiki'
    max_depth = 6
    frontier = list()
    visited = list()
    content = list()
    frontier.append(url)
    flag = 0
    current_depth = 0
    first_url_of_next_depth = url
    while len(visited) < 1000 and frontier != [] and current_depth <= max_depth:
        next_url = frontier[0]

        # Check to see if url has already been visited
        if next_url not in visited:

            # Check to see if depth has increased
            if next_url == first_url_of_next_depth:
                if current_depth != 0:
                    print("depth " + str(current_depth) + " crawled")
                current_depth = current_depth + 1
                print("crawling pages at depth:" + str(current_depth))
                flag = 1

            # for request rate of 1 request per second
            time.sleep(1)
            # Retrieve web page using beautiful soup
            r = requests.get(next_url)
            soup = BeautifulSoup(r.content)

            # Search for valid links within the page
            for link in soup.find_all("a"):
                parent = link.parent.name
                if parent == "p":
                    href = str(link.get("href"))
                    title = str(link.get("title"))
                    # Represent href in proper form using proper domain name
                    # Example /cyclone becomes https://en.wikipedia.org/wiki/cyclone
                    t = urljoin(base, href)

                    # Check if link already in frontier
                    if str(t) not in frontier:
                        # Check if link belongs to the same domain
                        if t.find(base) != -1:
                            # Check if the link points to contents on the same page
                            if t.find("#") == -1:
                                if keyword_in_link(keyword, href, title) == "true":
                                    # If all false add link to frontier
                                    frontier.append(str(t))
                                    # if flag is set update first_url_of_next_depth
                                    if flag == 1:
                                        first_url_of_next_depth = (str(t))
                                        flag = 0

            # Add crawled link to visited list
            visited.append(next_url)
            # Saving contents of visited page to content list
            '''soup.prettify()
            content.append("\n\n\n\n\nNEXT FILE")
            content.append(soup.find("title"))
            content.append("\n\n\n\n\n")
            content.append(soup)'''
        # Remove crawled link from frontier list
        frontier.remove(next_url)
    print("maximum depth reached: " + str(current_depth))
    save_to_file(frontier, visited, content)


def keyword_in_link(keyword, href, title):
    if href.lower().find(keyword) == 0 or title.lower().find(keyword) == 0 or \
                    href.lower().find("_" + keyword) != -1 or title.lower().find("_" + keyword) != -1 or \
                    href.lower().find("-" + keyword) != -1 or title.lower().find("-" + keyword) != -1 or \
                    href.lower().find(" " + keyword) != -1 or title.lower().find(" " + keyword) != -1:
        return "true"
    else:
        return "false"

# Code for saving contents of a list to a file-
# https://bbs.archlinux.org/viewtopic.php?id=75839


def save_to_file(frontier, visited, content):
    # Saving visited list to text file
    f = open("visited.txt", "w")
    f.write("\n".join(map(lambda x: str(x), visited)))
    f.close()

    # Saving frontier list to text file
    f = open("frontier.txt", "w")
    f.write("\n".join(map(lambda x: str(x), frontier)))
    f.close()

    # Saving contents list to file
    '''f = open("content.txt", "w")
    f.write("\n".join(map(lambda x: str(x), content)))
    f.close()'''


crawl("https://en.wikipedia.org/wiki/Tropical_cyclone", "rain")