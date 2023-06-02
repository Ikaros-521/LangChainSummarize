import os
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredURLLoader, UnstructuredPowerPointLoader, ReadTheDocsLoader, PyPDFLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks import get_openai_callback
from langchain.text_splitter import RecursiveCharacterTextSplitter


# 加载.env文件中的环境变量
load_dotenv()


def summarize_docs(docs, doc_url):
    print (f'You have {len(docs)} document(s) in your {doc_url} data')
    print (f'There are {len(docs[0].page_content)} characters in your document')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(docs)

    print (f'You have {len(split_docs)} split document(s)')

    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

    # print(OPENAI_API_KEY)

    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name="text-davinci-003")
    chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False)

    response = ""
    with get_openai_callback() as cb:
        response = chain.run(input_documents=split_docs)
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Successful Requests: {cb.successful_requests}")
        print(f"Total Cost (USD): ${cb.total_cost}")

    return response


loader = PyPDFLoader("ikaros.pdf")
pages = loader.load_and_split()
summarize_docs(pages[:10], "ikaros.pdf")