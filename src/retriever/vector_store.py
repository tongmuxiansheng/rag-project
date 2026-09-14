"""
向量数据库
功能：存储文本向量，支持相似度搜索
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict


class VectorStore:
    """向量数据库"""
    
    def __init__(self, collection_name: str = "rag_knowledge_base", persist_directory: str = "./chroma_db"):
        """
        初始化向量数据库
        :param collection_name: 集合名称
        :param persist_directory: 数据持久化目录
        """
        # 创建客户端，数据会保存到本地
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # 创建集合（类似数据库里的表）
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # 用余弦相似度
        )
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], metadatas: List[Dict] = None, ids: List[str] = None):
        """
        添加文档和向量到数据库
        :param documents: 文本列表
        :param embeddings: 对应的向量列表
        :param metadatas: 元数据列表（比如来源、页码等）
        :param ids: 文档ID列表
        """
        # 如果没传ID，自动生成
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        # 如果没传元数据，用空的
        if metadatas is None:
            metadatas = [{"source": "unknown"} for _ in range(len(documents))]
        
        # 添加到集合
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """
        搜索最相似的文档
        :param query_embedding: 查询文本的向量
        :param top_k: 返回最相似的前K条
        :return: 相似文档列表，每条包含文本、相似度、元数据
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # 整理结果
        output = []
        for i in range(len(results['documents'][0])):
            output.append({
                'document': results['documents'][0][i],
                'distance': results['distances'][0][i],  # 距离越小越相似
                'metadata': results['metadatas'][0][i],
                'id': results['ids'][0][i]
            })
        
        return output
    
    def count(self) -> int:
        """返回数据库中的文档数量"""
        return self.collection.count()
    
    def clear(self):
        """清空集合"""
        # 删除整个集合再重新创建
        collection_name = self.collection.name
        self.client.delete_collection(collection_name)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )



# 测试代码
if __name__ == "__main__":
    import sys
    import os
    # 把 embedding 目录直接加到路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    embedding_dir = os.path.join(os.path.dirname(current_dir), "embedding")
    sys.path.insert(0, embedding_dir)
    from embedding_service import EmbeddingService
    
    # 初始化向量化服务
    API_KEY = "a360ec3407834e0ab08d8d1773fec1e9.J1x2ggLa6i2ND2VM"
    embed_service = EmbeddingService(api_key=API_KEY)
    
    # 初始化向量数据库
    store = VectorStore(persist_directory="./test_chroma_db")
    
    # 清空测试数据
    store.clear()
    
    # 准备一些测试文档
    documents = [
        "Python是一种广泛使用的高级编程语言，以简洁易读著称。",
        "Java是一种面向对象的编程语言，广泛用于企业级应用开发。",
        "人工智能是计算机科学的一个分支，致力于创造能模拟人类智能的系统。",
        "机器学习是人工智能的一个子领域，让计算机从数据中学习。",
        "今天天气真好，适合出去散步。",
        "RAG（检索增强生成）结合了检索系统和大语言模型，能提供更准确的答案。"
    ]
    
    # 向量化
    print("正在向量化文档...")
    embeddings = embed_service.embed_batch(documents)
    
    # 添加到数据库
    print("正在存储到向量数据库...")
    store.add_documents(documents, embeddings)
    
    print(f"数据库中共有 {store.count()} 条文档")
    
    # 测试搜索
    query = "什么是RAG？"
    print(f"\n搜索查询: {query}")
    query_vec = embed_service.embed(query)
    results = store.search(query_vec, top_k=3)
    
    print("\n搜索结果（按相似度排序）：")
    for i, r in enumerate(results):
        similarity = 1 - r['distance']  # 距离转相似度
        print(f"\n第{i+1}名（相似度: {similarity:.4f}）:")
        print(f"  {r['document']}")
