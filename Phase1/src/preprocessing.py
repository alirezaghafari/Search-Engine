import json
from parsivar import Normalizer, Tokenizer, FindStems


def read_file(path):
    file = open(path)
    data = json.load(file)
    return data


def extract_contents(my_json):
    res = [documents[i]['content'] for i in my_json]
    return res


documents = read_file('../data/IR_data_news_12k.json')
contents = extract_contents(documents)
