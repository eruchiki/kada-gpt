import fitz
import re
import os
from glob import glob
from unicodedata import normalize
from langchain.text_splitter import RecursiveCharacterTextSplitter


def pdf_reader(file_path,skip_page=[],table_save=True,page_save=True):
    doc = fitz.open(file_path)
    filename = os.path.splitext(os.path.basename(file_path))[0]
    if page_save or table_save:
        output_dir = f"./data/{filename}"
        if not os.path.exists(output_dir):
            try:
                os.mkdir(output_dir)
            except OSError:
                dir_len = len(glob("./data/*")) + 1 
                os.mkdir(f"./data/{dir_len}")
    text_data = ""
    for page in range(len(doc)):
        page_data = doc[page]
        text = page_data.get_text()
        if page not in skip_page:
            text_data += page_data.get_text() +"\n"
        if page_save:
            with open(f"{output_dir}/{page}.txt",mode="w",encoding="utf-8") as f:
                f.write(text)
        table_data = page_data.find_tables()
        if len(table_data.tables) > 0 and table_save:
            table_text = ""
            for tbl in table_data:
                for t in tbl.extract():
                    if None in t:
                        t = [_t for _t in t if _t != None]
                    table_text += ":".join(t).replace("\n","") + "\n"
                table_text += "\n"
            with open(f"{output_dir}/table_{page}.txt",mode="w",encoding="utf-8") as f:
                f.write(table_text)
    return text_data

def normalize_text(text_data,remove_str="\u3000"):
    clean_text = normalize('NFKC', text_data)
    clean_text = re.sub(remove_str, r'', clean_text)
    return clean_text

def skip_text(text_data,skip_pattern):
    text_list = text_data.split("\n")
    result = []
    for text in text_list:
        text = text.replace("\n","")
        if text == "" or re.fullmatch(skip_pattern,text):
            continue
        else:
            result.append(text)
    return "\n".join(result)

def split_text(text_data,pattern):
    text_list = text_data.split("\n")
    result = []
    for text in text_list:
        if re.match(pattern,text):
            result.append("\n\n"+text)
        else:
            result.append(text)
    return "".join(result)

def chunk_split(text_data,chunk_num=1024,split_str="。.．"):
    # split_word = "["+split_str+"]"
    split_word = [sp for sp in split_str]+[""]
    text_data = text_data.replace("\n","")
    # text_data = re.sub(split_word , '\n', text_data)
    text_splitter = RecursiveCharacterTextSplitter(
    separators = split_word,
    chunk_size = chunk_num,
    chunk_overlap = 0
    )
    return text_splitter.split_text(text_data)


def sentence_split(text_data,split_str="。.．",sentence_num = 1):
    split_word = "["+split_str+"]"
    text_data = text_data.replace("\n","")
    text_data = re.sub(split_word , '\n', text_data)
    text_data = text_data.split("\n")
    return ["\n".join(text_data[t:t+sentence_num]) for t in range(0,len(text_data)-sentence_num+1,sentence_num)]

if __name__=="__main__":
    file_path = "test_pdf/20230721_mitsuda_ipsj_seminar2023.pdf"
    text_data = pdf_reader(file_path,table_save=False,page_save=False)
    with open("test.txt",mode="w",encoding="utf-8") as f:
        f.write(text_data)
