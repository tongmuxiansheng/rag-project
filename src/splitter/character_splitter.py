"""
按字符切片器
功能：把长文本按固定字符数切成小块
"""


class CharacterSplitter:
    """按字符切片器"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        初始化切片器
        :param chunk_size: 每块的字符数，默认500
        :param chunk_overlap: 相邻块之间重叠的字符数，默认50
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split(self, text: str) -> list:
        """
        把文本切成小块
        :param text: 输入的长文本
        :return: 切好的文本块列表
        """
        chunks = []
        start = 0
        
        while start < len(text):
            # 计算当前块的结束位置
            end = start + self.chunk_size
            
            # 取出这一块文本
            chunk = text[start:end]
            chunks.append(chunk)
            
            # 移动起始位置，减去重叠部分
            start = end - self.chunk_overlap
        
        return chunks


# 测试代码
if __name__ == "__main__":
    # 造一段长文本测试
    long_text = "这是一段测试文本。" * 100
    
    splitter = CharacterSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split(long_text)
    
    print(f"原文本长度: {len(long_text)} 字符")
    print(f"切成了 {len(chunks)} 块")
    for i, chunk in enumerate(chunks):
        print(f"第{i+1}块: {len(chunk)} 字符 - {chunk[:30]}...")
