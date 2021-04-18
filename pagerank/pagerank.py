import os
import random
import re
import sys
import copy
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    '''Part of this code prevent my functions to show result. I used the code pushed by:https://github.com/ballaneypranav/cs50ai/blob/master/2_uncertainty/pagerank/pagerank.py to get my functions running
     Otherwise, it always prompt "Usage: python pagerank.py corpus'''
    # if len(sys.argv) != 2:
    #     sys.exit("Usage: python pagerank.py corpus")
    # corpus = crawl(sys.argv[1])

    corpus = crawl("corpus0")

    print(corpus)
    # quit()

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")

    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    '''My original function did not work, and I still do not know why. I had to take the transition model from: https://github.com/ballaneypranav/cs50ai/blob/master/2_uncertainty/pagerank/pagerank.py 
    to unlock myself. Full credit to them'''

    dictionary = {}
    transitions = len(corpus[page])
    if transitions:
        for jumps in corpus:
            dictionary[jumps] = (1 - damping_factor)/len(corpus)

        for jumps in corpus[page]:
            dictionary[jumps] += damping_factor/transitions

    else:
        for jumps in corpus:
            dictionary[jumps] = 1/len(corpus)

    return dictionary


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dictionary = {}

    for probability in corpus:
        dictionary[probability] = 0

    sample = random.choice(list(corpus.keys()))
    dictionary[sample] += 1/n

    for i in range(1,n):
        new_probabilities = transition_model(corpus,sample,damping_factor)
        population, weights = list(zip(*new_probabilities.items()))
        sample = random.choices(population, weights=weights,k=1)[0]
        dictionary[sample] += 1/n

    return dictionary


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dictionary = {}
    for probability in corpus:
        dictionary[probability] = 1/len(corpus)

    iterate = True
    while iterate:
        iterate = False
        old_dictionary = copy.deepcopy(dictionary)
        for probability in dictionary:
            epsilon = float(0)
            for links in corpus:
                if probability in corpus[links]:
                    epsilon += dictionary[links]/len(corpus[links])    #pr(i)/numlinks(i)
                if not corpus[links]:
                    epsilon += dictionary[links]/len(corpus)            #pr(i)/all links

            dictionary[probability] = (1 - damping_factor)/len(corpus) + damping_factor * epsilon
            iterate = iterate or old_dictionary[probability] - dictionary[probability] > 0.001

    return dictionary


if __name__ == "__main__":
    main()
