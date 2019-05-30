from Document import Document
import WordList
from collections import defaultdict

def get_list_of_document(document_path):
    list_of_Document = []
    with open(document_path) as json_file:
        for line in json_file:
            if not (line[0] == "{" or line[0] == "}"):
                new_list = line.replace('"', " ").replace(':', " ").rstrip().split()
                docID = new_list[0]
                url = new_list[1]
                list_of_Document.append(Document(docID, url))
    return list_of_Document


def indexing(index_dict:dict,doc_list:["Document"]):
    total_doc_num = doc_list.length()
    for doc in doc_list:
        WordList.update_index_dict(index_dict,doc)
    WordList.calculate_tfidf(index_dict,total_doc_num)




if __name__ == "__main__":
	new_list = get_list_of_document("WEBPAGES_RAW\\bookkeeping.json")
	
	#dict{"word":{"docID":{"tf-idf":float,"line_num":[int],"cite":int}}}
	index_dict = defaultdict(dict)
	indexing(index_dict,new_list)
