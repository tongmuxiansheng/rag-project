"""
RAG 主流程
把文档加载、切片、向量化、检索、生成五个模块串起来
"""

import os
import sys

# 把 src 目录加到路径
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from loader.factory import get_loader
from splitter.recursive_splitter import RecursiveSplitter
from embedding.embedding_service import EmbeddingService
from retriever.vector_store import VectorStore
from generator.llm_generator import LLMGenerator


class RAGPipeline:
    """RAG 完整流程"""

    def __init__(self, api_key: str, persist_directory: str = "./chroma_db"):
        """
        初始化 RAG 系统
        :param api_key: DeepSeek API Key
        :param persist_directory: 向量数据库存储目录
        """
        # 初始化五个模块
        self.embedding_service = EmbeddingService()
        self.splitter = RecursiveSplitter(chunk_size=500, chunk_overlap=50)
        self.vector_store = VectorStore(persist_directory=persist_directory)
        self.generator = LLMGenerator(api_key=api_key)

        print("RAG 系统初始化完成")

    def ingest(self, file_path: str) -> int:
        """
        上传文档，处理后存入向量数据库
        :param file_path: 文档路径（支持 .txt / .pdf / .docx）
        :return: 存入的文档块数量
        """
        print(f"\n正在处理文档: {file_path}")

        # 第1步：加载文档
        print("  [1/4] 加载文档...")
        loader = get_loader(file_path)
        text = loader.load()
        print(f"  文档长度: {len(text)} 字符")

        # 第2步：文本切片
        print("  [2/4] 文本切片...")
        chunks = self.splitter.split(text)
        print(f"  切成了 {len(chunks)} 块")

        # 第3步：向量化
        print("  [3/4] 向量化...")
        embeddings = self.embedding_service.embed_batch(chunks)

        # 第4步：存入向量数据库
        print("  [4/4] 存入向量数据库...")
        metadatas = [{"source": os.path.basename(file_path), "chunk_id": i} for i in range(len(chunks))]
        ids = [f"{os.path.basename(file_path)}_{i}" for i in range(len(chunks))]
        self.vector_store.add_documents(chunks, embeddings, metadatas, ids)

        print(f"  完成！共存入 {len(chunks)} 块")
        return len(chunks)

    def query(self, question: str, top_k: int = 3, threshold: float = 0.35) -> dict:
        """
        用户提问，检索相关文档，生成答案
        :param question: 用户问题
        :param top_k: 检索最相关的前K条
        :param threshold: 相似度阈值，低于此值直接拒答（0-1，越高越严格）
        :return: 包含问题、答案、相关文档、置信度的字典
        """
        print(f"\n问题: {question}")

        # 第1步：把问题向量化
        print("  [1/3] 问题向量化...")
        question_vec = self.embedding_service.embed(question)

        # 第2步：检索相关文档
        print("  [2/3] 检索相关文档...")
        results = self.vector_store.search(question_vec, top_k=top_k)
        print(f"  找到 {len(results)} 条相关文档")

        # 计算最高相似度（distance越小越相似，相似度 = 1 - distance）
        if results:
            max_similarity = 1 - results[0]['distance']
            print(f"  最高相似度: {max_similarity:.4f}（阈值: {threshold}）")
        else:
            max_similarity = 0.0
            print("  未找到任何文档")

        # 第2.5步：相似度阈值判断——太低就直接拒答，不传给大模型
        if max_similarity < threshold:
            print(f"  相似度低于阈值 {threshold}，直接拒答")
            answer = (
                f"抱歉，知识库中没有找到与您问题相关的内容。\n"
                f"（当前最高相似度为 {max_similarity:.2f}，低于阈值 {threshold}）\n"
                f"建议：换个问法试试，或上传相关文档后再提问。"
            )
            result = {
                'question': question,
                'answer': answer,
                'sources': [],
                'confidence': max_similarity,
                'threshold': threshold,
                'answered': False
            }
            print("\n" + "=" * 50)
            print("回答:")
            print(answer)
            print("=" * 50)
            return result

        # 第3步：生成答案（相似度够高才调用大模型）
        print("  [3/3] 生成答案...")
        result = self.generator.generate_with_sources(question, results)

        # 添加置信度信息
        result['confidence'] = max_similarity
        result['threshold'] = threshold
        result['answered'] = True

        print("\n" + "=" * 50)
        print("回答:")
        print(result['answer'])
        print(f"\n置信度: {max_similarity:.4f}")
        print("\n参考来源:")
        for i, src in enumerate(result['sources']):
            print(f"  {i + 1}. {src.get('source', '未知')} (块{src.get('chunk_id', '?')})")
        print("=" * 50)

        return result

    def get_document_count(self) -> int:
        """获取数据库中的文档块数量"""
        return self.vector_store.count()


# 测试代码
if __name__ == "__main__":
    # 从环境变量读取 API Key
    API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
    if not API_KEY:
        print("请设置 DEEPSEEK_API_KEY 环境变量")
        sys.exit(1)

    # 初始化 RAG 系统（用测试数据库，避免污染正式库）
    rag = RAGPipeline(api_key=API_KEY, persist_directory="./test_rag_db")

    # 清空测试库
    rag.vector_store.clear()

    # 上传测试文档
    test_file = r"D:\AI_Agent三个项目初始结构\rag-project\data\test.pdf"
    if os.path.exists(test_file):
        rag.ingest(test_file)
    else:
        print(f"测试文件不存在: {test_file}")
        print("请先把 test.pdf 放到 data 目录下")

    # 提问测试
    if rag.get_document_count() > 0:
        print("\n" + "#" * 60)
        print("# 测试1：问资料里有的问题（应该正常回答）")
        print("#" * 60)
        rag.query("RAG的关键组件有哪些？")

        print("\n" + "#" * 60)
        print("# 测试2：问资料里没有的问题（应该拒答）")
        print("#" * 60)
        rag.query("秦始皇哪年统一六国？")
