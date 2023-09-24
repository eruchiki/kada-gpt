import fitz
import re
import os
from glob import glob
from unicodedata import normalize

def pdf_reader(file_path,skip_page=[],table_save=True,page_save=True):
    doc = fitz.open(file_path)
    filename = os.path.splitext(os.path.basename(file_path))[0]
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

def sentence_split(text_data,split_str="。"):
    text_list = text_data.split("\n")
    result = []
    for text in text_list:
        if text[-1]==split_str:
            result.append(text+"\n")
        else:
            result.append(text)
    return "".join(result)