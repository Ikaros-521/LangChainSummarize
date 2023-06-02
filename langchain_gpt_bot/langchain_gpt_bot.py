from langchain import OpenAI
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
import sys
import os
from dotenv import load_dotenv


# 加载.env文件中的环境变量
load_dotenv()

def indexDirectory(directory_path):
    """
        max_input_size：最大输入大小。它定义了模型接受的文本输入的最大长度（以标记数量为单位）。如果输入文本超过这个长度，将会被截断或缩短到最大长度。
        num_outputs：输出摘要的数量。它确定了模型生成的摘要输出的数量。通常，你可以指定你希望生成的摘要句子或标记的数量。
        max_chunk_overlap：最大块重叠。在进行文本摘要时，输入文本通常会被分成多个块（chunks）进行处理。此参数定义了允许的最大块之间的重叠数量。较高的重叠可以确保在块之间保持上下文的连续性，但也可能导致重复的摘要内容。
        chunk_size_limit：块大小限制。它定义了每个块的最大大小（以标记数量为单位）。输入文本将根据此大小进行分块处理。
    """
    # set maximum input size
    max_input_size = 4096
    #set number of output tokens
    num_outputs = 1000
    #set maximum chunk overlap
    max_chunk_overlap = 100
    #set chunk size limit
    chunk_size_limit = 600

    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

    # define LLM 选择的模型为 text-davinci-003
    # 语言模型 "text-davinci-003" 的功能主要是帮助创建一个将文档转化为向量表示的搜索索引，而不是直接回答用户的问题。
    # 模型的知识主要用于理解和表示文档的语义内容，以便在用户输入查询时能够找到最相关的文档。
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY, model_name="text-davinci-003" , max_tokens=num_outputs))
    # 帮助生成模型输入的提示
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    # 读取和处理目录中的文档
    # 如果在创建索引之后，有新的文档添加到目录中，或者有其他源的数据需要查询，那么这些数据是无法被系统获取和处理的。
    documents = SimpleDirectoryReader(directory_path).load_data()
    # ServiceContext封装了文本索引和检索服务的配置和上下文信息。
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    #index = GPTSimpleVectorIndex(documents,llm_predictor=llm_predictor,prompt_helper=prompt_helper)
    # 负责使用语言模型进行文本索引和检索。
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
    # 将创建的索引保存到磁盘上的'index.json'文件中
    index.save_to_disk('index.json')

    return index


# 接收用户的输入查询，并返回相关的回答。
def ask_ai():
    # 从磁盘上的'index.json'文件中加载搜索索引
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    while True:
        query = input("提问:")
        # 使用索引来找到最相关的答案，并将其打印出来
        response = index.query(query,response_mode="compact")
        print(f"回答:{response}")


if __name__ == "__main__":
    # 传入文件夹路径
    indexDirectory(sys.argv[1])
    ask_ai()
