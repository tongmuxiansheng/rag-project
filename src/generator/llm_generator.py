"""
LLM 生成器
功能：把检索到的相关文档和用户问题传给大模型，生成答案
使用 DeepSeek API
"""

import os
from openai import OpenAI


class LLMGenerator:
    """大模型生成器（DeepSeek版）"""

    def __init__(self, api_key: str = None, base_url: str = "https://api.deepseek.com", model: str = "deepseek-chat"):
        """
        初始化生成器
        :param api_key: DeepSeek API Key
        :param base_url: API 地址，默认 DeepSeek
        :param model: 模型名称，默认 deepseek-chat
        """
        if api_key is None:
            api_key = os.getenv("DEEPSEEK_API_KEY", "")

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model

    def generate(self, question: str, context: str) -> str:
        """
        根据问题和上下文生成答案
        :param question: 用户问题
        :param context: 检索到的相关文档内容
        :return: 大模型生成的答案
        """
        # 构造 prompt，告诉模型基于给定的资料回答
        prompt = f"""你是一个专业的问答助手。请根据下面提供的参考资料回答用户的问题。

【参考资料】
{context}

【用户问题】
{question}

【回答要求】
1. 只根据参考资料中的内容回答，不要编造资料中没有的信息
2. 如果参考资料中没有相关信息，请回答"根据现有资料无法回答这个问题"
3. 回答要简洁明了，分点说明
4. 答案用中文

请给出你的回答："""

        # 调用大模型
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # 温度低，回答更稳定
            max_tokens=2000
        )

        return response.choices[0].message.content

    def generate_with_sources(self, question: str, documents: list) -> dict:
        """
        生成答案并附带来源
        :param question: 用户问题
        :param documents: 检索到的文档列表，每个元素是字典，包含 document 和 metadata
        :return: 包含答案和来源的字典
        """
        # 把文档拼接成上下文
        context_parts = []
        for i, doc in enumerate(documents):
            source = doc.get('metadata', {}).get('source', f'文档{i+1}')
            context_parts.append(f"[来源{i+1}: {source}]\n{doc['document']}")
        context = "\n\n".join(context_parts)

        # 生成答案
        answer = self.generate(question, context)

        return {
            'question': question,
            'answer': answer,
            'sources': [doc.get('metadata', {}) for doc in documents]
        }


# 测试代码
if __name__ == "__main__":
    import os
    API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
    if not API_KEY:
        print("请设置 DEEPSEEK_API_KEY 环境变量")
        exit(1)

    generator = LLMGenerator(api_key=API_KEY)

    # 模拟检索到的文档
    test_documents = [
        {
            'document': 'RAG（检索增强生成）结合了检索系统和大语言模型，能提供更准确的答案。',
            'metadata': {'source': 'AI技术文档.pdf', 'page': 1}
        },
        {
            'document': 'RAG的工作流程是：先把文档切片并存入向量数据库，用户提问时检索相关片段，再让大模型基于这些片段生成答案。',
            'metadata': {'source': 'AI技术文档.pdf', 'page': 2}
        },
        {
            'document': 'Python是一种广泛使用的高级编程语言。',
            'metadata': {'source': '编程入门.pdf', 'page': 1}
        }
    ]

    # 测试问答
    question = "什么是RAG？它的工作流程是什么？"
    print(f"问题: {question}\n")

    result = generator.generate_with_sources(question, test_documents)

    print("回答:")
    print(result['answer'])
    print("\n参考来源:")
    for i, src in enumerate(result['sources']):
        print(f"  {i+1}. {src.get('source', '未知')} (第{src.get('page', '?')}页)")
