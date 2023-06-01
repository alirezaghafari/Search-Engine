from itertools import permutations
from indexing import get_positional_indexed
from preprocessing import preprocess, documents
import re

positional_index = get_positional_indexed()


def process_phrase(tokens):
    result = []
    for biword  in permutations(tokens, 2):
        word1 = biword[0]
        word2 = biword[1]
        if (word1 not in positional_index.keys()) or (word2 not in positional_index.keys()):
            return []

        index1 = tokens.index(word1)
        index2 = tokens.index(word2)
        pos_dic_1 = positional_index.get(word1).pos
        pos_dic_2 = positional_index.get(word2).pos
        difference = abs(index1 - index2)

        docs = positional_intersect(pos_dic_1, pos_dic_2, difference)

        if len(result) != 0:
            result = list(set(result) & set(docs))
        else:
            result = docs

    return result

def positional_intersect(pos_dict_1 ,  pos_dict_2 , k):
    doc_id_1=list(pos_dict_1.keys())
    doc_id_2=list(pos_dict_2.keys())
    doc_id_1.sort()
    doc_id_2.sort()

    result = []
    i, j = 0, 0

    while i < len(doc_id_1)  and  j < len(doc_id_2):
        id_1 = doc_id_1[i]
        id_2 = doc_id_2[j]
        if id_1 == id_2:
            pos1 = pos_dict_1[id_1]
            pos2 = pos_dict_2[id_2]
            for pos in pos1:
                if pos + k  in  pos2  or  pos - k in pos2:
                    result.append(id_1)
            i , j = i + 1 , j + 1
        elif id_1 < id_2:
            i += 1
        else:
            j += 1

    return result

def excluded_terms(query):
    query_terms = query.split()
    index_of_exclamation_mark = [i for i in range(len(query_terms)) if query_terms[i] == '!']
    index_of_excluded_terms = [query_terms[i + 1] for i in index_of_exclamation_mark]
    return index_of_excluded_terms


def ranking(phrases=[] , not_words=[] , terms=[]):
    rank = {}

    for token in terms:
        if token in positional_index.keys():
            for doc_id in  positional_index[token].pos.keys():
                if doc_id in  rank.keys():
                    rank[doc_id] += 1
                else:
                    rank[doc_id] = 1

    for item in phrases:

        for doc_id in process_phrase(item):
            if doc_id in rank.keys():
                rank[doc_id] += 1
            else:
                rank[doc_id] = 1

    docs_with_excluded_words = []
    for word in not_words:
        doc_ids = positional_index[word].pos.keys()
        for doc_id in doc_ids:
            docs_with_excluded_words.append(doc_id)

    if len(rank) != 0:
        for doc in docs_with_excluded_words:
            if doc in rank.keys():
                del rank[doc]

    rank = dict(sorted(rank.items(), key=lambda a: a[1], reverse=True))

    return rank


def search_query(query):
    query = ' '.join(preprocess([query])[0])
    phrases = find_phrases(query)
    flat_phrases = [item for sublist in phrases for item in sublist]
    excluded_words = excluded_terms(query)
    query = query.replace('!', '')
    query = query.replace('"', '')
    query_terms = query.split()
    terms_to_look_up = []
    for x in query_terms:
        if x not in flat_phrases and x not in excluded_words:
            terms_to_look_up.append(x)
    result = ranking(phrases=phrases, not_words=excluded_words, terms=terms_to_look_up)
    return result

def find_phrases(query):
    phrases_list = []
    reg = re.compile('"[^"]*"')
    for each_phrase in reg.findall(query):
        each_phrase = each_phrase.replace('"', '').strip().split()
        phrases_list.append(each_phrase)
    return phrases_list

def print_result(output_dict):
    doc_id = list(output_dict.keys())[:5]
    for i in range(len(doc_id)):
        print(f'result {i + 1}: ')
        url = documents[str(doc_id[i])]['url']
        title = documents[str(doc_id[i])]['title']
        print('title: ', title, '\nurl: ', url)
        print('\n############\n')



