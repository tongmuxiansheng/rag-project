"""
Excel 文件加载器
功能：读取 .xlsx / .xls 文件，提取所有工作表的数据
"""

try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False


class ExcelLoader:
    """Excel 文件加载器"""

    def __init__(self, file_path: str):
        """
        初始化加载器
        :param file_path: Excel 文件的路径
        """
        self.file_path = file_path

    def load(self) -> str:
        """
        加载 Excel 文件，提取所有工作表的数据
        :return: Excel 的纯文本内容
        """
        if not OPENPYXL_AVAILABLE:
            raise ImportError("请安装 openpyxl：pip install openpyxl")

        wb = openpyxl.load_workbook(self.file_path, data_only=True)
        all_text = []

        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            sheet_content = [f"=== 工作表：{sheet_name} ==="]

            for row in sheet.iter_rows(values_only=True):
                # 过滤掉全空的行
                if not row or all(cell is None or str(cell).strip() == '' for cell in row):
                    continue
                # 把每个单元格的内容用 | 分隔
                cells = [str(cell).strip() if cell is not None else '' for cell in row]
                sheet_content.append(" | ".join(cells))

            if len(sheet_content) > 1:
                all_text.append("\n".join(sheet_content))

        wb.close()
        return "\n\n".join(all_text)


# 测试代码
if __name__ == "__main__":
    loader = ExcelLoader(r"D:\AI_Agent三个项目初始结构\rag-project\data\test.xlsx")
    text = loader.load()
    print(text)
    print(f"\n总共读取了 {len(text)} 个字符")
