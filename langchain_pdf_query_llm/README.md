# langchain_gpt_bot

## 环境
系统：win10  
python：3.10.8  
依赖：`pip install langchain openai PyPDF2 faiss-cpu tiktoken`  

## 配置
`.env`中配置你的`OPENAI_API_KEY`
```
OPENAI_API_KEY=<your valid openai api key>
```

修改源码中`PdfReader`传入的pdf路径  

## 运行
`python langchain_pdf_query_llm.py`  

## 效果
```
以下是chunk_size=500的情况，回答更加的详细，但是消耗的token也更多，费钱

提问：阿斯特蕾亚和伊卡洛斯的关系
Output: 阿斯特蕾亚和伊卡洛斯相处友好，却怕惹伊卡洛斯生气（害怕伊卡洛斯的力量）。
Total Tokens: 2128
Prompt Tokens: 2070
Completion Tokens: 58
Successful Requests: 1
Total Cost (USD): $0.004255999999999999



以下是chunk_size=100的情况，回答很简单，但是消耗的token大幅降低，虽然省了钱，但是有点太简单了。不过有些场景用用感觉还行。

(py3-10-8) E:\GitHub_pro\LangChainSummarize\langchain_pdf_query_llm>python langchain_pdf_query_llm.py
文档前100个字符：伊卡洛斯，《天降之物》中的女主角之一，型号 α“ ” “ ”，自称是 娱乐用万能天使 ，其实是 战略用万能天使 ，
“ ” 西纳普斯称她为 空之女王 。西纳普斯人畏惧其强大的能力而被封印，后被代达罗斯
共切分为83块文本内容
提问：阿斯特蕾亚和伊卡洛斯的关系
Output: 友好相处。
Total Tokens: 615
Prompt Tokens: 610
Completion Tokens: 5
Successful Requests: 1
Total Cost (USD): $0.00123
提问：



gpt3.5的回答

问：阿斯特蕾亚和伊卡洛斯的关系
答：在希腊神话中，阿斯特蕾亚（Astraea）和伊卡洛斯（Icarus）之间并没有直接的关系。阿斯特蕾亚是一位女神，被认为是正义和纯洁的化身。她是天空的守护者，同时也是维持人类与神灵之间秩序的力量。

伊卡洛斯是代达罗斯的儿子，他和他的父亲一起设计了一对能够让他们飞翔的翅膀。然而，伊卡洛斯在飞行时过于骄傲和冲动，不听从父亲的忠告，飞得太接近太阳，导致翅膀融化而坠落。他的故事是关于自负和不谨慎的警示。

所以，阿斯特蕾亚和伊卡洛斯在神话中并没有直接的联系，他们分别代表了不同的概念和故事。
```

## 致谢
源自 [BV1XV4y1f7js](https://www.bilibili.com/video/BV1XV4y1f7js)  
源自 [BV1xX4y1B7Vt](https://www.bilibili.com/video/BV1xX4y1B7Vt)  