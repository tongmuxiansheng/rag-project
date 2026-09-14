"""
向量化服务
功能：把文本转换成向量（embedding），使用本地免费模型 BAAI/bge-small-zh-v1.5
不需要 API Key，第一次运行会自动下载模型（约100MB）
"""

import os
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """向量化服务（本地模型版）"""

    def __init__(self, api_key: str = None, base_url: str = None, model_name: str = "BAAI/bge-small-zh-v1.5"):
        """
        初始化向量化服务
        :param api_key: 兼容参数，本地模型不需要，传了也忽略
        :param base_url: 兼容参数，本地模型不需要
        :param model_name: 模型名称，默认 bge-small-zh-v1.5（中文轻量模型，512维）
        """
        print(f"正在加载本地向量化模型: {model_name} ...")
        print("（第一次运行会自动下载模型，约100MB，请耐心等待）")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        print("模型加载完成！")

    def embed(self, text: str) -> list:
        """
        把单条文本转换成向量
        :param text: 输入文本
        :return: 向量（列表形式）
        """
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: list) -> list:
        """
        批量把多条文本转换成向量
        :param texts: 文本列表
        :return: 向量列表
        """
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vectors]

    def get_dimension(self) -> int:
        """获取向量维度"""
        vec = self.embed("test")
        return len(vec)


# 测试代码
if __name__ == "__main__":
    service = EmbeddingService()

    # 测试单条向量化
    text = "人工智能正在改变世界"
    vector = service.embed(text)
    print(f"文本: {text}")
    print(f"向量维度: {len(vector)}")
    print(f"向量前5个值: {vector[:5]}")

    # 测试批量向量化
    texts = ["我喜欢Python", "我喜欢Java", "今天天气真好"]
    vectors = service.embed_batch(texts)
    print(f"\n批量向量化 {len(texts)} 条文本")
    for i, (t, v) in enumerate(zip(texts, vectors)):
        print(f"  第{i+1}条: {t} -> 维度{len(v)}")

    # 计算相似度
    import numpy as np
    v1 = np.array(vectors[0])
    v2 = np.array(vectors[1])
    v3 = np.array(vectors[2])

    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    print(f"\n相似度测试:")
    print(f"  '我喜欢Python' 和 '我喜欢Java' 相似度: {cosine_sim(v1, v2):.4f}")
    print(f"  '我喜欢Python' 和 '今天天气真好' 相似度: {cosine_sim(v1, v3):.4f}")
    print(f"  （意思越相近，相似度越高）")
