from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.schema import Document
    
def websearch(query, websearch_num):
    search = GoogleSearchAPIWrapper()

    tool = Tool(
        name="Google Search",
        description="Search Google for recent results.",
        func=search.run,
    )
    
    websearch_results = search.results(query, websearch_num)
    # print(websearch_results)

    relate_info = []
    for i, content in enumerate(websearch_results):
        info = Document(
            page_content=content['snippet'],
            metadata={"filename":content['title'], "link":content['link']}
        )
        
    relate_info.append(info)

    return relate_info