"""
TXT 文件加载器
功能：读取 .txt 文件，返回纯文本内容
"""

class TxtLoader:
    """TXT 文件加载器"""
    
    def __init__(self, file_path: str):
        """
        初始化加载器
        :param file_path: TXT 文件的路径
        """
        self.file_path = file_path
    
    def load(self) -> str:
        """
        加载文件，返回文本内容
        :return: 文件的纯文本内容
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content


# 测试代码
if __name__ == "__main__":
    # 先在 data 目录下放一个 test.txt 文件，里面随便写点内容
    loader = TxtLoader("../../data/test.txt")
    text = loader.load()
    print(text)
