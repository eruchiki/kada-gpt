from langchain.schema import Document


def text_to_documents(text_list,metadata):
    return [Document(page_content = data,metadata = metadata) for data in text_list]
    
def documents_search(db,query,top_k=3,filter=None,border=0.7):
    docs = db.similarity_search_with_score(query=query, k=top_k,filter=filter)
    print([(doc.page_content,score) for doc,score in docs])
    return [doc.page_content for doc,score in docs if score > border],[score for doc,score in docs if score > border]