# Third-Party Imports
import nltk
import torch

from transformers import BertForQuestionAnswering, BertTokenizer, AutoTokenizer
from sentence_transformers import SentenceTransformer, util

# Standard Library Imports
import os
from string import punctuation
from math import log1p

class BertQa():

    def __init__(self):
        self._corpus = dict()
        self._file_matches = 1
        self._sentence_matches = 1
    
    def load_files(self, dirname):
        main_path = os.path.join(os.path.dirname(__file__), dirname)
        file_dict = dict()

        for file in os.listdir(main_path):
            with open(os.path.join(main_path, file), 'r') as f:
                file_dict[file] = f.read()
        
        return file_dict
    
    def _cosine_similarity(self, text_1, text_2, model):
        embedding_1= model.encode(text_1, convert_to_tensor=True)
        embedding_2 = model.encode(text_2, convert_to_tensor=True)
    
        return float(util.pytorch_cos_sim(embedding_1, embedding_2))
    
    def _compute_idfs(self, fnames):
        file_idfs = dict()
        unique_words = set()
        num_docs = len(fnames)

        for name in fnames:
            unique_words = set().union(unique_words, set(self._corpus[name]))
        
        for word in unique_words:
            num_apps = sum(1 for name in fnames if word in self._corpus[name])
            file_idfs[word] = log1p(num_docs / num_apps)
        
        return file_idfs

    def _top_files_idf(self, query, idfs):
        tf_idfs = { fname: 0 for fname in self._corpus }

        for w in query:
            for fname in self._corpus:
                tf_idfs[fname] += self._corpus[fname].count(w) * idfs.get(w, 0)
        
        ranked_scores = sorted(
            tf_idfs.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [score[0] for score in ranked_scores][:self._file_matches]
    
    def _top_files_cosine(self, query, fnames):
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        ranked_files = sorted([
            (name, self._cosine_similarity(query, self._corpus[name], model))
            for name in fnames
            reverse=True
        ])

        return ranked_files