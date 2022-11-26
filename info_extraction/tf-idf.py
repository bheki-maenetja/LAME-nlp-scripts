# Third-Party Imports
import nltk

# Standard Library Imports
import sys
import os
from string import punctuation
from math import log1p

# Local Imports
from queries import get_text_cli

def main():
    # Calculate IDF values across files
    files = load_files()
    file_words = { fname: tokenize(files[fname]) for fname in files }
    for key, val in file_words.items():
        print("New File =====================")
        print(key, val, end="\n\n")
    # Prompt user for input query
    # Determine top file matches according to TF-IDF
    # Extract sentences from top files
    # Compute IDF values across sentences
    # Determine top sentence matches

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

def compute_idfs():
    pass

def top_files():
    pass

if __name__ == "__main__":
    main()