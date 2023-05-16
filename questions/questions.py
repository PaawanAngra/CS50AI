import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dictionary = {}
    for file in os.listdir(os.path.join(os.getcwd(), directory)):
        with open (os.path.join(os.getcwd(), directory, file)) as f:
            dictionary[file] = f.read()
            f.close()
    return dictionary   


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document.lower())
    final_words = []
    for word in words:
        if word not in nltk.corpus.stopwords.words("english"):
            temp = ''
            for c in word:
                if c not in string.punctuation:
                    temp += c
            if temp != '':
                final_words.append(word.lower())
    return final_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total_documents = len(documents)
    word_documents = {}
    for document in documents:
        for word in documents[document]:
            if word not in word_documents:
                word_documents[word] = set()
                word_documents[word].add(document)
            else:
                word_documents[word].add(document)
    idfs = {}
    for word in word_documents:
        idfs[word] = math.log(total_documents / len(word_documents[word]))
    return idfs

                
def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf = {}
    for file in files:
        tfidf[file] = 0
    for word in query:
        for file in files:
            frequency = 0
            for file_word in files[file]:
                if word == file_word:
                    frequency += 1
            score = frequency * idfs[word]
            tfidf[file] += score
    temp = []
    final = []
    for file in sorted(tfidf, key=tfidf.get, reverse=True):
        temp.append(file)
    for i in range(n):
        final.append(temp[i])
    return final



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf_score = {}
    qtd = {}
    for sentence in sentences:
        idf_score[sentence] = 0
    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                idf_score[sentence] += idfs[word]
    for sentence in sentences:
        q = 0
        for word in query:
            if word in sentences[sentence]:
                q += 1
        qtd[sentence] = q/len(sentences[sentence])
    temp = []
    final = []
    sorted_sentences =  sorted(idf_score, key=idf_score.get, reverse=True)
    temp = sorted_sentences
    for i in range(len(sorted_sentences) - 1):
        if idf_score[sorted_sentences[i]] == idf_score[sorted_sentences[i + 1]]:
            if qtd[sorted_sentences[i]] <= qtd[sorted_sentences[i + 1]]:
                temp_sentence = temp[i]
                temp[i] = temp[i+1]
                temp[i+1] = temp_sentence
    for i in range(n):
        final.append(temp[i])
    return final
                

if __name__ == "__main__":
    main()
