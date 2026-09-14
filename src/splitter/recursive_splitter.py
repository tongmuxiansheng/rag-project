"""
递归切片器
功能：优先按段落切，段落太长按句子切，句子还太长按字符切
"""


class RecursiveSplitter:
    """递归切片器"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        初始化切片器
        :param chunk_size: 每块的最大字符数
        :param chunk_overlap: 相邻块之间重叠的字符数
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # 分隔符优先级：段落 > 句子 > 逗号 > 空格 > 字符
        self.separators = ["\n\n", "\n", "。", "！", "？", ".", "，", " ", ""]
    
    def split(self, text: str) -> list:
        """
        递归切分文本
        :param text: 输入的长文本
        :return: 切好的文本块列表
        """
        chunks = []
        self._split_text(text, chunks)
        return chunks
    
    def _split_text(self, text: str, chunks: list):
        """
        递归切分的内部方法
        """
        # 如果文本已经小于块大小，直接加进去
        if len(text) <= self.chunk_size:
            if text.strip():
                chunks.append(text.strip())
            return
        
        # 找到合适的分隔符
        separator = self._find_separator(text)
        
        if separator:
            # 用分隔符把文本分成小片段
            pieces = text.split(separator)
            current_chunk = ""
            
            for piece in pieces:
                # 如果当前块加上这个片段还没超大小，就加进去
                if len(current_chunk) + len(piece) + len(separator) <= self.chunk_size:
                    current_chunk += piece + separator
                else:
                    # 当前块满了，保存，然后开始新块
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    # 如果这个片段本身就比块大，递归切这个片段
                    if len(piece) > self.chunk_size:
                        self._split_text(piece, chunks)
                        current_chunk = ""
                    else:
                        current_chunk = piece + separator
            # 处理最后一块
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
        else:
            # 没有合适的分隔符，就按字符硬切
            for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
                chunk = text[i:i + self.chunk_size]
                if chunk.strip():
                    chunks.append(chunk.strip())
    
    def _find_separator(self, text: str) -> str:
        """
        找到文本中存在的最高优先级分隔符
        """
        for sep in self.separators:
            if sep and sep in text:
                return sep
        return ""


# 测试代码
if __name__ == "__main__":
    # 造一段有段落有句子的文本
    long_text = """这是第一段。这是第一段的第二句话。这是第一段的第三句话，这句话比较长，用来测试切片效果。

这是第二段。这是第二段的第二句话。这是第二段的第三句话。

这是第三段。这是第三段的第二句话。""" * 10
    
    splitter = RecursiveSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split(long_text)
    
    print(f"原文本长度: {len(long_text)} 字符")
    print(f"切成了 {len(chunks)} 块")
    for i, chunk in enumerate(chunks):
        print(f"\n第{i+1}块 ({len(chunk)}字符):")
        print(chunk[:80] + "..." if len(chunk) > 80 else chunk)
