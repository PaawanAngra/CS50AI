import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
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
    
    probability_distribution = {}
    total_pages = len(corpus)
    for x in corpus:
        probability_distribution[x] = (1-damping_factor)/total_pages

    pages_linked = corpus[page]
    for x in pages_linked:
        probability_distribution[x] += damping_factor/len(pages_linked)
    
    return probability_distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = [x for x in corpus]
    probability_distribution = {}
    
    for x in pages:
        probability_distribution[x] = 0
    
    current_page = random.choice(pages)
    probability_distribution [current_page] += 1
    
    for i in range(n-1):
        transistion_probability = transition_model(corpus, current_page, DAMPING)
        probabilities = [transistion_probability[x] for x in pages]
        current_page = random.choices(pages,weights = probabilities, k=1)
        current_page = current_page[0]
        probability_distribution[current_page] += 1

    for x in probability_distribution:
        probability_distribution[x] = probability_distribution[x]/n
    
    return probability_distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probability_distribution = {}
    
    for x in corpus:
        probability_distribution[x] = 1/len(corpus)
    
    corpus_reverse = {}
    for x in corpus:
        corpus_reverse[x] = []
    for x in corpus:
        link_to = corpus[x]
        for i in link_to:
            corpus_reverse[i].append(x)

    change = True
    while(change):
        change = False
        for i in corpus:
            new_probability = (1-damping_factor)/len(corpus)
            pages_from = corpus_reverse[i]
            for j in pages_from:
                new_probability += (damping_factor * probability_distribution[j])/len(corpus[j])
            difference = abs(new_probability - probability_distribution[i])
            probability_distribution[i] = new_probability
            if difference > 0.001:
                change = True

    return probability_distribution



if __name__ == "__main__":
    main()
