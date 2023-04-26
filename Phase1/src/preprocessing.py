import json
from parsivar import Normalizer, Tokenizer, FindStems

def read_file(path):
    file = open(path)
    data = json.load(file)
    return data



documents = read_file('../data/IR_data_news_12k.json')