"""
PDF 文件加载器
功能：读取 .pdf 文件，返回纯文本内容
"""

from pypdf import PdfReader


class PDFLoader:
    """PDF 文件加载器"""
    
    def __init__(self, file_path: str):
        """
        初始化加载器
        :param file_path: PDF 文件的路径
        """
        self.file_path = file_path
    
    def load(self) -> str:
        """
        加载 PDF 文件，返回所有页面的文本内容
        :return: PDF 的纯文本内容
        """
        # 创建 PDF 读取器
        reader = PdfReader(self.file_path)
        
        # 用来存所有页面的文本
        all_text = []
        
        # 遍历每一页
        for page in reader.pages:
            # 提取这一页的文本
            page_text = page.extract_text()
            all_text.append(page_text)
        
        # 把所有页面的文本用换行连起来
        return "\n".join(all_text)


# 测试代码
if __name__ == "__main__":
    # 先在 data 目录下放一个 test.pdf 文件
    loader = PDFLoader(r"D:\AI_Agent三个项目初始结构\rag-project\data\test.pdf")
    text = loader.load()
    print(text)
    print(f"\n总共读取了 {len(text)} 个字符")
