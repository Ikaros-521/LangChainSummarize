from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS

import os
from dotenv import load_dotenv


# 加载.env文件中的环境变量
load_dotenv()

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# location of the pdf file/files. 
# 加载本地的pdf文件
reader = PdfReader('../docs/伊卡洛斯百度百科.pdf')

# read data from the file and put them into a variable called raw_text
# 读取数据存入raw_text
raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

# print(raw_text)

print("文档前100个字符：" + raw_text[:100])

# We need to split the text that we read into smaller chunks so that during information retreival we don't hit the token size limits. 
# 我们需要将读取的文本分成更小的块，这样在信息检索过程中就不会达到令牌大小的限制。
text_splitter = CharacterTextSplitter(
    # 拆分文本的分隔符
    separator = "\n",
    # 每个文本块的最大字符数
    chunk_size = 100,
    # 两个相邻文本块之间的重叠字符数
    # 这种重叠可以帮助保持文本的连贯性，特别是当文本被用于训练语言模型或其他需要上下文信息的机器学习模型时
    chunk_overlap  = 50,
    # 用于计算文本块的长度
    # 在这里，长度函数是len，这意味着每个文本块的长度是其字符数。在某些情况下，你可能想要使用其他的长度函数。
    # 例如，如果你的文本是由词汇组成的，你可能想要使用一个函数，其计算文本块中的词汇数，而不是字符数。
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

print("共切分为" + str(len(texts)) + "块文本内容")

# 创建了一个OpenAIEmbeddings实例，然后使用这个实例将一些文本转化为向量表示（嵌入）。
# 然后，这些向量被加载到一个FAISS（Facebook AI Similarity Search）索引中，用于进行相似性搜索。
# 这种索引允许你在大量向量中快速找到与给定向量最相似的向量。
embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_texts(texts, embeddings)

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate

# 使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道或者你在文章中找不到答案，不要试图编造答案。
prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know or you can't find the answer in the article, don't try to make up an answer.

{context}

Question: {question}
Answer in Chinese:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# 创建一个询问-回答链（QA Chain），使用了一个自定义的提示模板
chain = load_qa_chain(ChatOpenAI(model_name="gpt-3.5-turbo-0301", openai_api_key=OPENAI_API_KEY), chain_type="stuff", prompt=PROMPT)

def query_func(str):
  with get_openai_callback() as cb:
    query = str
    # 将用户的查询进行相似性搜索，并使用QA链运行
    docs = docsearch.similarity_search(query)

    # 可以打印匹配的文档内容，看看
    # print(docs)

    res = chain.run(input_documents=docs, question=query)

    # 相关消耗和费用
    print(f"Output: {res}")
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Successful Requests: {cb.successful_requests}")
    print(f"Total Cost (USD): ${cb.total_cost}")


while True:
    query = input("提问：")
    query_func(query)

# 当用户输入一个查询时，这个系统首先会在本地文档集合中进行相似性搜索，寻找与查询最相关的文档。
# 然后，它会把这些相关文档以及用户的查询作为输入，传递给语言模型。这个语言模型会基于这些输入生成一个答案。
# 如果系统在本地文档集合中找不到任何与用户查询相关的文档，或者如果语言模型无法基于给定的输入生成一个有意义的答案，
# 那么这个系统可能就无法回答用户的查询。