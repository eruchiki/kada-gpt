import fitz
import re
import os
from glob import glob
from unicodedata import normalize
from langchain.text_splitter import RecursiveCharacterTextSplitter


def pdf_reader(file_data,skip_page=[],table_save=True):
    doc = fitz.open(stream=file_data.read(), filetype="pdf")

    text_data = ""
    for page in range(len(doc)):
        page_data = doc[page]
        if page not in skip_page:
            text_data += page_data.get_text()
        table_data = page_data.find_tables()
        if len(table_data.tables) > 0 and table_save:
            table_text = ""
            for tbl in table_data:
                for t in tbl.extract():
                    if None in t:
                        t = [_t for _t in t if _t != None]
                    table_text += ":".join(t).replace("\n","") + "\n"
                table_text += "\n"
    return text_data

def normalize_text(text_data,replace_str="\u3000"):
    clean_text = normalize('NFKC', text_data)
    clean_text = clean_text.replace(replace_str, ' ')
    clean_text = clean_text.replace('\n', '')
    return clean_text

# OpenAIのtoken数と同等のチャンクサイズで計算
def chunk_split(text_data,token_num=1000):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        separators = ["\n","。","．",".","、","，",",", ""],
        model_name="gpt-3.5-turbo",
        keep_separator = True,
        chunk_size = token_num,
        chunk_overlap = 0
    )
    split_text = text_splitter.split_text(text_data)
    for i in range(1, len(split_text)):
        split_text[i-1] += split_text[i][0]
        split_text[i] = split_text[i][1:]
    return split_text
