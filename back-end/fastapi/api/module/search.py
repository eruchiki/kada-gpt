from langchain.schema import Document
import MeCab
import pykakasi
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


def morpheme(sentence: str) -> tuple[dict, list]:
    wakati = MeCab.Tagger(f"-Owakati -d {NEOLOGD_PATH} -r {MECABRC_PATH}")
    morpheme_list = []
    morpheme_dict: dict = {}
    kks = pykakasi.kakasi()
    node = wakati.parseToNode(sentence)
    while node:
        word = node.surface
        if word != "":
            morpheme_list.append(word)
        kind_dict = {}
        node_list = node.feature.split(",")
        if node_list[1] == "数詞":
            kind_dict = {"speech": node_list[0], "detail_speech": node_list[1]}
        else:
            reading = kks.convert(node_list[-2])
            kind_dict = {
                "speech": node_list[0],
                "detail_speech": node_list[1:4],
                "endform": node_list[-3],
                "reading": reading[0]["hira"],
            }
            if len(node_list) > 5:
                kind_dict["endform"] = node_list[-3]
                kind_dict["reading"] = reading[0]["hira"]
        if word not in morpheme_dict.keys():
            morpheme_dict[word] = kind_dict
        node = node.next
    return morpheme_dict, morpheme_list
