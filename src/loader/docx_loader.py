"""
Word 文件加载器
功能：读取 .docx 文件，返回纯文本内容
"""

from docx import Document


class DocxLoader:
    """Word 文件加载器"""
    
    def __init__(self, file_path: str):
        """
        初始化加载器
        :param file_path: Word 文件的路径
        """
        self.file_path = file_path
    
    def load(self) -> str:
        """
        加载 Word 文件，返回所有段落的文本内容
        :return: Word 的纯文本内容
        """
        # 打开 Word 文档
        doc = Document(self.file_path)
        
        # 用来存所有段落的文本
        all_text = []
        
        # 遍历每一个段落
        for para in doc.paragraphs:
            # 只添加非空段落
            if para.text.strip():
                all_text.append(para.text)
        
        # 把所有段落用换行连起来
        return "\n".join(all_text)


# 测试代码
if __name__ == "__main__":
    loader = DocxLoader(r"D:\AI_Agent三个项目初始结构\rag-project\data\test.docx")
    text = loader.load()
    print(text)
    print(f"\n总共读取了 {len(text)} 个字符")
