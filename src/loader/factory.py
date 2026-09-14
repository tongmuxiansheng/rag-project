"""
文档加载器工厂
根据文件后缀自动选择对应的加载器
支持 .txt / .pdf / .docx / .xlsx / .xls
"""

import os
from .txt_loader import TxtLoader
from .pdf_loader import PDFLoader
from .docx_loader import DocxLoader
from .excel_loader import ExcelLoader


def get_loader(file_path: str, use_ocr: bool = False):
    """
    根据文件后缀自动选择加载器
    :param file_path: 文件路径
    :param use_ocr: 是否启用 OCR（仅对 PDF 有效，识别图片中的文字）
    :return: 对应的加载器实例
    """
    # 获取文件后缀，转小写
    ext = os.path.splitext(file_path)[1].lower()

    # 根据后缀选择加载器
    if ext == '.txt':
        return TxtLoader(file_path)
    elif ext == '.pdf':
        return PDFLoader(file_path, use_ocr=use_ocr)
    elif ext == '.docx':
        return DocxLoader(file_path)
    elif ext in ['.xlsx', '.xls']:
        return ExcelLoader(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {ext}，目前支持 .txt / .pdf / .docx / .xlsx / .xls")


def get_supported_formats():
    """获取支持的文件格式列表"""
    return ['.txt', '.pdf', '.docx', '.xlsx', '.xls']


# 测试代码
if __name__ == "__main__":
    base_path = r"D:\AI_Agent三个项目初始结构\rag-project\data"

    # 测试 TXT
    print("=== 测试 TXT ===")
    loader = get_loader(os.path.join(base_path, "test.txt"))
    print(loader.load()[:100] + "...")

    # 测试 PDF
    print("\n=== 测试 PDF ===")
    loader = get_loader(os.path.join(base_path, "test.pdf"))
    text = loader.load()
    print(f"PDF 总字符数: {len(text)}")

    # 测试 Word
    print("\n=== 测试 Word ===")
    loader = get_loader(os.path.join(base_path, "test.docx"))
    text = loader.load()
    print(f"Word 总字符数: {len(text)}")

    print("\n所有加载器测试通过！")
