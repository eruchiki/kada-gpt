from unicodedata import normalize
from langchain.text_splitter import RecursiveCharacterTextSplitter
# import MeCab
import tiktoken


NEOLOGD_PATH = "/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"
MECABRC_PATH = "/etc/mecabrc"


def num_tokens_from_string(string: str, model_name: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def normalize_text(text_data: str, replace_str: str = "\u3000") -> str:
    clean_text = normalize("NFKC", text_data)
    clean_text = clean_text.replace(replace_str, " ")
    clean_text = clean_text.replace("\n", "")
    return clean_text


def chunk_split(text_data: str, chunk_num: int = 500) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        separators=["\n\n", "\n", "。", "．", "."],
        model_name="gpt-4",
        keep_separator=True,
        chunk_size=chunk_num,
        chunk_overlap=0,
    )
    split_text = text_splitter.split_text(text_data)
    for i in range(1, len(split_text)):
        split_text[i - 1] += split_text[i][0]
        split_text[i] = split_text[i][1:]
    return split_text


# def morpheme(sentence: str, neologd: bool = False) -> tuple[dict, list]:
#     if neologd:
#         wakati = MeCab.Tagger(NEOLOGD_PATH)
#     else:
#         wakati = MeCab.Tagger("-Owakati")
#     kks = pykakasi.kakasi()
#     morpheme_list = []
#     morpheme_dict: dict = {}
#     node = wakati.parseToNode(sentence)
#     while node:
#         word = node.surface
#         if word != "":
#             morpheme_list.append(word)
#         kind_dict: dict = {}
#         node_list = node.feature.split(",")
#         if neologd:
#             if node_list[1] == "数詞":
#                 kind_dict = {
#                     "speech": node_list[0],
#                     "detail_speech": node_list[1],
#                 }
#             else:
#                 reading = kks.convert(node_list[-2])
#                 kind_dict = {
#                     "speech": node_list[0],
#                     "detail_speech": node_list[1:4],
#                     "endform": node_list[-3],
#                     "reading": reading[0]["hira"],
#                 }
#                 if len(node_list) > 5:
#                     kind_dict["endform"] = node_list[-3]
#                     kind_dict["reading"] = reading[0]["hira"]
#         else:
#             kind_dict = {
#                 "speech": node_list[0],
#                 "detail_speech": node_list[1:4],
#             }
#             if len(node_list) > 7:
#                 kind_dict["inflect"] = node_list[5]
#                 kind_dict["endform"] = node_list[7]
#                 reading = kks.convert(node_list[-1])
#                 kind_dict["reading"] = reading[0]["hira"]
#             else:
#                 kind_dict["inflect"] = "*"
#                 kind_dict["endform"] = "*"
#                 reading = kks.convert(node_list[-1])
#                 kind_dict["reading"] = reading[0]["hira"]
#         if word not in morpheme_dict.keys():
#             morpheme_dict[word] = kind_dict
#         node = node.next
#     return morpheme_dict, morpheme_list
