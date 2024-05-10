import fitz
# from api.module.preprocessing import morpheme
from fastapi import UploadFile
import aiofiles


def pdf_reader(file_data: UploadFile, table_save: bool = False) -> str:
    doc = fitz.open(stream=file_data.file.read(), filetype="pdf")
    text_data = ""
    for page in range(len(doc)):
        page_data = doc[page]
        text_data += page_data.get_text()
        # if page_delete(page_data.get_text()):
        #     text_data += page_data.get_text()
        if table_save:
            table_data = page_data.find_tables()
            if len(table_data.tables) == 0:
                continue
            table_text = ""
            for tbl in table_data:
                for t in tbl.extract():
                    if None in t:
                        t = [_t for _t in t if _t is not None]
                    table_text += ":".join(t).replace("\n", "") + "\n"
                table_text += "\n"
    return text_data


# def page_delete(page_text: str) -> bool:
#     speech_list = [
#         "名詞",
#         "動詞",
#         "形容詞",
#         "形容動詞",
#         "副詞",
#         "助詞",
#         "助動詞",
#         "記号",
#         "数詞",
#     ]
#     mor_kind, mor_list = morpheme(page_text, neologd=True)
#     page_speech = [mor_kind[mor]["speech"] for mor in mor_list]
#     speech_count = [page_speech.count(speech) for speech in speech_list]
#     speech_rate = [speech / sum(speech_count) for speech in speech_count]
#     if speech_rate[0] > 0.7 or speech_rate[1] < 0.02:
#         return True
#     else:
#         return False


async def async_create_file_with_data(path: str, data: UploadFile) -> None:
    async with aiofiles.open(path, "wb") as f:
        await f.write(data.file.read())
