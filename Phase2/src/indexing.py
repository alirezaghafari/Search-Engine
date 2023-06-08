from preprocessing import *
import math
import numpy as np
from preprocessing import preprocess, documents


class Term:
    def __init__(self):
        self.freq_in_doc = {}
        self.pos = {}
        self.freq_in_all_docs = 0
        self.weight_in_doc = {}
        self.champ_list = {}

    def posting(self, position, doc_id):
        if doc_id not in self.pos:
            self.pos[doc_id] = []
            self.freq_in_doc[doc_id] = 0
        self.freq_in_all_docs += 1
        self.freq_in_doc[doc_id] += 1
        self.pos[doc_id].append(position)

    def get_docs(self):
        return self.pos.keys()

    def set_weight(self, doc_id, number_of_docs):
        self.weight_in_doc[doc_id] = tfidf_score_function(
            self, doc_id, number_of_docs)

    def create_champions_list(self, length):
        self.champ_list = dict(
            sorted(self.weight_in_doc.items(), key=lambda _input: _input[1], reverse=True)[:length])

    def get_champ_list(self):
        return self.champ_list