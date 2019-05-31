from nltk.corpus import stopwords
from main import load_dict
from WordList import common_line_num
import math

STOPWORDS = set(stopwords.words('english'))

class Cosine_computation:
    def __init__(self, query_list:[]):
        self.query_list = self.eliminate_stop_words(query_list)
        self.word_dict = load_dict("WordList.txt")
        self.query_frequence_dict = self.get_query_frequency()
        #dict{"word":{"docID":{"tf-idf":float,"line_num":[int],"cite":int}}}
        
    def ranking(self) -> list:
        #score_dict = defaultdict(float)
        #query_length = len(query_list)
        query_normalization_vector = dict()
        doc_normalization_vector = defaultdict()
        cosine_score_dict = dict()
        total_score_dict = dict()
        
        for query in set(self.query_list):
            query_frequency = self.query_frequence_dict[query]
            query_normalization_vector[query] = query_frequency/self.get_query_normalization()  #query_normalization    
    
            if query in word_dict.keys():      
                for docID, inner_dict in word_dict[query].items():
                    doc_normalization_vector[docID].add({query: inner_dict})
                    # dict{"docID": {"tf-idf":float,"line_num":[int],"cite":int}
            
                for docID, inner_dict in doc_normalization_vector.items():   #term_normalization
                    total_score = 0
                    cosine_score = 0
                    for term in inner_dict.keys():
                        total_score += inner_dict[term]["tf-idf"]**2
                    tf_idf_score_normalization = math.sqrt(total_score)
                    for term in inner_dict.keys():
                        inner_dict[term]["tf-idf-normal"] = inner_dict[term]["tf-idf"]/tf_idf_score_normalization
                        cosine_score += inner_dict[term]["tf-idf-normal"] * query_normalization_vector[term]
                    cosine_score_dict[docID] = cosine_score
                    # dict {"docID": cosine_score}
############################################# cosine score ############################################
        
        for docID in cosine_score_dict.keys():
            line_num_list = doc_normalization_vector[docID]["line_num"]
            cite = doc_normalization_vector[docID]["cite"]
            line_num_score = self.get_line_num_score(line_num_list)
            cite_score = self.get_cite_score(cite)
            total_score_dict[docID] = cosine_score_dict[docID] + line_num_score + cite_score
        return sorted(total_score_dict.keys(), key=lambda x: total_score_dict[x], reverse=True)
        
    
    def eliminate_stop_words(self, query_list):
        new_list = []
        for query in query_list:
            if (query not in STOPWORDS):
                new_list.append(query)
        return new_list
    
    def get_query_frequency(self):
        frequency_dict = defaultdict(int)
        for query in self.query_list:
            frequency_dict[query] += 1
        for key, value in frequency_dict.items():
            frequency_dict[key] = 1 + math.log10(value)
        return frequency_dict
    
    def get_query_normalization(self, query_frequency: int):
        total_num = 0
        for query in self.query_frequence_dict.values():
            total_num += query**2
        return math.sqrt(total_num)
    
    def get_line_num_score(self, number_list: list):
        return common_line_num(number_list) / len(self.query_list) * 0.5
    
    def get_cite_score(self, cite: int):
        return cite * 0.05
        