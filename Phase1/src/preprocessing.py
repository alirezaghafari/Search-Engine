import json
from parsivar import Normalizer, Tokenizer, FindStems


def read_file(path):
    file = open(path)
    data = json.load(file)
    return data


def extract_contents(my_json):
    res = [documents[i]['content'] for i in my_json]
    return res

def persian_stopwords(path):
    with open(path) as my_file:
        list_ = my_file.read().splitlines()
    return list_

documents = read_file('../data/IR_data_news_12k.json')
contents = extract_contents(documents)
stopwords_list = persian_stopwords("../data/stopwords.txt")
stopwords_set = {stopwords_list[i] for i in range(0, len(stopwords_list))}
