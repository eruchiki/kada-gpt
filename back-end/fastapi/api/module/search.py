from langchain.schema import Document
from typing import Optional
from langchain.vectorstores import Qdrant
from api.module.preprocessing import chunk_split

NEOLOGD_PATH = "/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"
MECABRC_PATH = "/etc/mecabrc"


def documents_search(
    db: Qdrant,
    query: str,
    top_k: int = 3,
    filter: Optional[dict] = None,
    border: float = 0.7,
) -> tuple[list, list]:
    docs = db.similarity_search_with_score(query=query, k=top_k, filter=filter)
    # print([(doc.page_content,score) for doc,score in docs])
    related_data = [doc for doc, score in docs if score > border]
    score_data = [score for doc, score in docs if score > border]
    for i, item in enumerate(related_data):
        item.metadata["rank"] = i
    return related_data, score_data


def detail_search(related_data: list) -> list:
    for relate in related_data:
        group = []
        related_info = []
        split_text = chunk_split(relate.page_content)
        for i, text in enumerate(split_text):
            info = Document(
                page_content=text,
                metadata={
                    "filename": relate.metadata["filename"],
                    "rank": relate.metadata["rank"],
                    "item_number": i,
                },
            )
            group.append(info)
        related_info.append([group])
    return related_info
