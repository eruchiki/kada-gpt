from unicodedata import normalize
from langchain.text_splitter import RecursiveCharacterTextSplitter


def normalize_text(text_data: str, replace_str: str = "\u3000") -> str:
    clean_text = normalize("NFKC", text_data)
    clean_text = clean_text.replace(replace_str, " ")
    clean_text = clean_text.replace("\n", "")
    return clean_text


def chunk_split(text_data: str, chunk_num: int = 6) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "．", "."],
        keep_separator=True,
        chunk_size=chunk_num,
        chunk_overlap=0,
    )
    split_text = text_splitter.split_text(text_data)
    for i in range(1, len(split_text)):
        split_text[i - 1] += split_text[i][0]
        split_text[i] = split_text[i][1:]
    return split_text
