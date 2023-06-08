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


def indexing(dictionary):
    terms_map = {}
    for doc_id in range(len(dictionary)):
        for pos in range(len(dictionary[doc_id])):
            term = dictionary[doc_id][pos]
            if term in terms_map:
                term_obj = terms_map[term]
            else:
                term_obj = Term()
            term_obj.posting(pos, doc_id)
            terms_map[term] = term_obj

    return terms_map


def calculate_tf(term, doc_id):
    freq = term.freq_in_doc[doc_id]
    if freq > 0:
        return 1 + math.log10(freq)
    return 0


def calculate_idf(term, number_of_docs):
    n = len(term.freq_in_doc)
    return math.log10(number_of_docs/n)


def tfidf_score_function(term, doc_id, number_of_docs):
    return calculate_tf(term, doc_id) * calculate_idf(term, number_of_docs)


def calculate_weights(dictionary, number_of_docs):
    for term in dictionary:
        postings_list = dictionary[term].get_docs()
        for doc_id in postings_list:
            dictionary[term].set_weight(doc_id, number_of_docs)


def calculate_tf_for_query(term, tokens):
    freq = 0
    for word in tokens:
        if word == term:
            freq += 1
    if freq > 0:
        return 1 + math.log10(freq)
    return 0



def champions_list(dictionary, r):
    for term in dictionary:
        dictionary[term].create_champions_list(r)




def get_docs_norm(dictionary, number_of_docs):
    lengths = np.zeros(number_of_docs)
    for term in dictionary:
        for doc_id, weight in dictionary[term].weight_in_doc.items():
            lengths[int(doc_id)] += weight ** 2
    return np.sqrt(lengths)




def cosine_similarity(query_terms, dictionary, number_of_docs, norms):
    scores = {}
    for term in query_terms:
        query_tfidf = calculate_tf_for_query(
            term, query_terms) * calculate_idf(dictionary[term], number_of_docs)
        for doc_id, doc_score in dictionary[term].get_champ_list().items():
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += query_tfidf * doc_score

    for doc_id in scores:
        scores[doc_id] /= norms[int(doc_id)]
    return scores

def jaccard_similarity(query_tokens,dictionary):
    scores = {}
    for term in query_tokens:
        docs = list(dictionary[term].freq_in_doc.keys())
        for doc_id in docs:
            if doc_id not in scores:
                intersection = len(list(set(terms_dictionary[doc_id]) & set(query_tokens)))
                union = len(list(set(terms_dictionary[doc_id]))) + len(set(query_tokens))
                score = intersection/union
                scores[doc_id] = score
    return scores



def print_result(socres, k):
    best_related_docs = dict(
        sorted(socres.items(), key=lambda item: item[1], reverse=True)[:k])
    for doc_id in best_related_docs:
        title = documents[str(doc_id)]['title']
        url = documents[str(doc_id)]['url']
        print('title: ', title, '\nurl: ', url)
        print('****************')



terms_dictionary = preprocessed_docs
positional_index = indexing(terms_dictionary)
calculate_weights(positional_index, len(contents))
champions_list(positional_index, 60)
docs_norms = get_docs_norm(positional_index, len(contents))





query = "شاگرد آنتونیو کونته"
query_tokens = preprocess([query])[0]
scores = jaccard_similarity(query_tokens,positional_index)
# scores = cosine_similarity(
#     query_tokens, positional_index, len(contents), docs_norms)
print_result(scores, k=5)
