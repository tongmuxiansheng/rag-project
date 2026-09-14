"""
PDF 文件加载器（升级版）
功能：读取 .pdf 文件，提取文本和表格，支持 OCR 识别图片文字
使用 pdfplumber 替代 pypdf，表格提取效果更好
"""

import os
import tempfile
from typing import Optional

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

# OCR 相关（可选，需要安装 easyocr）
OCR_AVAILABLE = False
ocr_engine = None


def init_ocr():
    """初始化 OCR 引擎（懒加载，第一次使用时才初始化）"""
    global OCR_AVAILABLE, ocr_engine
    if OCR_AVAILABLE:
        return True
    try:
        import easyocr
        # 支持中文简体和英文
        ocr_engine = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        OCR_AVAILABLE = True
        print("[OCR] EasyOCR 初始化成功")
        return True
    except Exception as e:
        print(f"[OCR] EasyOCR 不可用：{e}")
        OCR_AVAILABLE = False
        return False


class PDFLoader:
    """PDF 文件加载器（支持文本+表格+OCR）"""

    def __init__(self, file_path: str, use_ocr: bool = False):
        """
        初始化加载器
        :param file_path: PDF 文件的路径
        :param use_ocr: 是否启用 OCR 识别图片文字（默认关闭，需要时开启）
        """
        self.file_path = file_path
        self.use_ocr = use_ocr
        if use_ocr:
            init_ocr()

    def load(self) -> str:
        """
        加载 PDF 文件，提取所有页面的文本和表格
        :return: PDF 的纯文本内容（含表格）
        """
        if PDFPLUMBER_AVAILABLE:
            return self._load_with_pdfplumber()
        elif PYPDF_AVAILABLE:
            print("[警告] pdfplumber 未安装，使用 pypdf（表格提取效果较差）")
            return self._load_with_pypdf()
        else:
            raise ImportError("请安装 pdfplumber 或 pypdf：pip install pdfplumber")

    def _load_with_pdfplumber(self) -> str:
        """使用 pdfplumber 加载（表格提取效果好）"""
        all_text = []

        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_content = []

                # 1. 提取普通文本
                text = page.extract_text()
                if text:
                    page_content.append(text)

                # 2. 提取表格（pdfplumber 的强项）
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables, 1):
                    if table and len(table) > 0:
                        table_text = self._table_to_text(table)
                        page_content.append(f"\n【表格{table_idx}】\n{table_text}")

                # 3. OCR 识别图片中的文字（如果启用）
                if self.use_ocr and OCR_AVAILABLE:
                    ocr_text = self._ocr_page(page)
                    if ocr_text:
                        page_content.append(f"\n【图片文字识别】\n{ocr_text}")

                if page_content:
                    all_text.append(f"--- 第 {page_num} 页 ---\n" + "\n".join(page_content))

        return "\n\n".join(all_text)

    def _load_with_pypdf(self) -> str:
        """使用 pypdf 加载（备用方案）"""
        reader = PdfReader(self.file_path)
        all_text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                all_text.append(page_text)
        return "\n".join(all_text)

    def _table_to_text(self, table) -> str:
        """
        把表格转换成纯文本，保留行列结构
        :param table: pdfplumber 返回的表格（二维列表）
        :return: 格式化的表格文本
        """
        lines = []
        for row in table:
            # 过滤掉全空的行
            if not row or all(cell is None or str(cell).strip() == '' for cell in row):
                continue
            # 把每个单元格的内容用 | 分隔
            cells = [str(cell).strip() if cell else '' for cell in row]
            lines.append(" | ".join(cells))
        return "\n".join(lines)

    def _ocr_page(self, page) -> Optional[str]:
        """
        对页面进行 OCR 识别，提取图片中的文字
        :param page: pdfplumber 的页面对象
        :return: OCR 识别到的文字
        """
        if not OCR_AVAILABLE or ocr_engine is None:
            return None

        try:
            # 把页面转成图片
            img = page.to_image(resolution=200)
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name
            img.save(tmp_path)

            # OCR 识别（easyocr 格式：[bbox, text, confidence]）
            result = ocr_engine.readtext(tmp_path)
            os.unlink(tmp_path)

            # 提取识别到的文字
            texts = []
            if result:
                for item in result:
                    if len(item) >= 2:
                        texts.append(item[1])  # item[1] 是识别到的文字

            return "\n".join(texts) if texts else None
        except Exception as e:
            print(f"[OCR] 识别出错：{e}")
            return None


# 测试代码
if __name__ == "__main__":
    loader = PDFLoader(r"D:\AI_Agent三个项目初始结构\rag-project\data\test.pdf")
    text = loader.load()
    print(text)
    print(f"\n总共读取了 {len(text)} 个字符")
