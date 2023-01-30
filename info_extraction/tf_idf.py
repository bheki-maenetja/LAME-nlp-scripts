# Third-Party Imports
import nltk

# Standard Library Imports
import sys
import os
from string import punctuation
from math import log1p

# Local Imports
from queries import get_text_cli

# Global Variables
FILE_MATCHES = 1
SENTENCE_MATCHES = 1

def main():
    # Calculate IDF values across files
    files = load_files()
    file_words = { fname: tokenize(files[fname]) for fname in files }
    file_idfs = compute_idfs(file_words)   

    # Prompt user for input query
    query = set(tokenize(get_text_cli("Your query")))

    # Determine top file matches according to TF-IDF
    top_fnames = top_files(query, file_words, file_idfs, FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for fname in top_fnames:
        for passage in files[fname].split('\n'):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    sent_idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, sent_idfs, SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory="corpus"):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    main_path = os.path.join(os.path.dirname(__file__), directory)
    file_dict = dict()

    for file in os.listdir(main_path):
        with open(os.path.join(main_path, file), 'r') as f:
            file_dict[file] = f.read()
    
    return file_dict

def tokenize(doc):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.
    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    banned = list(punctuation) + nltk.corpus.stopwords.words("english")

    return [
        w.lower() for w in nltk.word_tokenize(doc)
        if w.lower() not in banned
    ]

def compute_idfs(docs):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.
    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    file_idfs = dict()
    unique_words = set()
    num_docs = len(docs)

    for doc in docs:
        unique_words = set().union(unique_words, set(docs[doc]))
    
    for word in unique_words:
        num_apps = sum(1 for doc in docs if word in docs[doc])
        file_idfs[word] = log1p(num_docs / num_apps)
    
    return file_idfs

def top_files(query, docs, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf
    """
    tf_idf_scores = { doc: 0 for doc in docs }

    for w in query:
        for doc in docs:
            tf_idf_scores[doc] += docs[doc].count(w) * idfs.get(w, 0)
    
    ranked_scores = sorted(
        tf_idf_scores.items(), 
        key=lambda x: x[1], 
        reverse=True
    )

    return [score[0] for score in ranked_scores][:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sent_scores = { sent: [0,0] for sent in sentences }

    for sent in sentences:
        common_words = query.intersection(set(sentences[sent]))
        sent_scores[sent][1] = len(common_words)
        sent_scores[sent][0] = sum(idfs.get(w, 0) for w in common_words)
    
    ranked_scores = sorted(
        sent_scores.items(),
        key=lambda x: (x[1][0], x[1][1]),
        reverse=True
    )

    return [score[0] for score in ranked_scores][:n]

if __name__ == "__main__":
    main()