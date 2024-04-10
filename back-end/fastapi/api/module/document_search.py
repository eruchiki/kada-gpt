from typing import Optional
from langchain_community.vectorstores import Qdrant
from langchain_community.retrievers import BM25Retriever


def documents_search(
    db: Qdrant,
    query: str,
    top_k: int = 3,
    filter: Optional[dict] = None,
    border: float = 0.7,
) -> list:
    docs = db.similarity_search_with_score(query=query, k=top_k, filter=filter)
    # print([(doc.page_content,score) for doc,score in docs])
    related_data = [doc for doc, score in docs if score > border]
    score_data = [score for doc, score in docs if score > border]
    with open("test2.txt", "w") as f:
        f.write(str(related_data).encode().decode("unicode-escape"))
    for i, item in enumerate(related_data):
        item.metadata["rank"] = i
    return [related_data, score_data]


def bm25_search(query: str, retriever: BM25Retriever) -> list:
    related_data = retriever.get_relevant_documents(query)
    return related_data
