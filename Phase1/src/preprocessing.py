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


my_normalizer = Normalizer()
my_tokenizer = Tokenizer()
stemmer = FindStems()


def preprocess(contents_):
    preprocessed_docs = []

    for content in contents_:
        # normalizing
        normalized = my_normalizer.normalize(content)
        content_tokens = my_tokenizer.tokenize_words(normalized)
        tokens = []
        for token in content_tokens:
            # stemming
            token = stemmer.convert_to_stem(token)
            # remove stopwords
            if token in stopwords_set:
                continue
            tokens.append(token)
        preprocessed_docs.append(tokens)

    return preprocessed_docs


documents = read_file('../data/IR_data_news_12k.json')
contents = extract_contents(documents)
stopwords_list = persian_stopwords("../data/stopwords.txt")
stopwords_set = {stopwords_list[i] for i in range(0, len(stopwords_list))}
preprocessed_docs = preprocess(contents)
