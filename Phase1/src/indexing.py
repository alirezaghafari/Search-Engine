from preprocessing import get_tokens

class Term:
    def __init__(self, number_of_docs):
        self.freq_in_doc  =  {i: 0 for i in range(number_of_docs)}
        self.pos  =  {}
        self.freq_in_all_docs  =  0


    def posting(self, position, doc_id):
        if doc_id not in self.pos:
            self.pos[doc_id] = []
        self.freq_in_all_docs += 1
        self.freq_in_doc[doc_id] += 1
        self.pos[doc_id].append(position)

        
def indexing(dictionary):
    terms_map  =  {}
    return terms_map

terms_dictionary  =  get_tokens()
positional_index  =  indexing(terms_dictionary)