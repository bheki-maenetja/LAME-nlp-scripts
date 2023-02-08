# Third-Party Imports
import nltk
import torch

from transformers import BertForQuestionAnswering, BertTokenizer, AutoTokenizer
from sentence_transformers import SentenceTransformer, util

# Standard Library Imports
import os
from string import punctuation
from math import log1p