# -*- coding: utf-8 -*-
"""
生成 RAG 知识库系统搭建全过程详解文档（完整更新版）
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import parse_xml

doc = Document()

# ========== 全局样式设置 ==========
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style.font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

# 标题样式
for level in range(1, 4):
    h_style = doc.styles[f'Heading {level}']
    h_style.font.name = '微软雅黑'
    h_style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    h_style.font.color.rgb = RGBColor(0x1A, 0x2E, 0x4B)

doc.styles['Heading 1'].font.size = Pt(20)
doc.styles['Heading 2'].font.size = Pt(16)
doc.styles['Heading 3'].font.size = Pt(13)

# 页面边距
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.8)
    section.right_margin = Cm(2.8)


def add_body(text, bold=False, size=11):
    """添加正文段落"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(size)
    run.bold = bold
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    return p


def add_code(code_text):
    """添加代码块"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    # 灰色背景
    shading = parse_xml(
        '<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'w:val="clear" w:color="auto" w:fill="F5F5F5"/>'
    )
    p._p.get_or_add_pPr().append(shading)
    return p


def add_table(headers, rows, col_widths=None):
    """添加表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # 表头
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(10)
                run.font.name = '微软雅黑'
                run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

    # 数据行
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)
                    run.font.name = '微软雅黑'
                    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)

    doc.add_paragraph()
    return table


def add_callout(text, color="E8F4FD"):
    """添加提示框"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(10.5)
    shading = parse_xml(
        f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        f'w:val="clear" w:color="auto" w:fill="{color}"/>'
    )
    p._p.get_or_add_pPr().append(shading)
    # 左边框
    pBdr = parse_xml(
        '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:left w:val="single" w:sz="24" w:space="8" w:color="1A2E4B"/>'
        '</w:pBdr>'
    )
    p._p.get_or_add_pPr().append(pBdr)
    return p


# ==================== 封面 ====================
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_before = Pt(120)
run = title.add_run('RAG 知识库系统')
run.font.name = '微软雅黑'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
run.font.size = Pt(36)
run.bold = True
run.font.color.rgb = RGBColor(0x1A, 0x2E, 0x4B)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('搭建全过程详解')
run.font.name = '微软雅黑'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
run.font.size = Pt(24)
run.font.color.rgb = RGBColor(0x66, 0x7E, 0xEA)

doc.add_paragraph()
doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = info.add_run('从0到1完整复现指南\n包含六大核心模块 + FastAPI接口 + 前端页面 + Docker部署')
run.font.name = '微软雅黑'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
run.font.size = Pt(13)
run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

doc.add_page_break()

# ==================== 目录页 ====================
doc.add_heading('目录', level=1)
toc_items = [
    '第一章  项目概述',
    '第二章  环境准备',
    '第三章  项目结构',
    '第四章  模块一：文档加载器（loader）',
    '第五章  模块二：文本切片器（splitter）',
    '第六章  模块三：向量化（embedding）',
    '第七章  模块四：向量数据库（retriever）',
    '第八章  模块五：LLM生成器（generator）',
    '第九章  模块六：主流程（pipeline）',
    '第十章  FastAPI 接口封装',
    '第十一章  前端页面开发',
    '第十二章  Docker 部署',
    '第十三章  模型切换说明（智谱API → 本地模型+DeepSeek）',
    '第十四章  从0到1完整复现步骤',
    '第十五章  常见问题与解决方案',
    '第十六章  简历描述参考',
]
for item in toc_items:
    p = doc.add_paragraph()
    run = p.add_run(item)
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(12)
    p.paragraph_format.line_spacing = 1.8

doc.add_page_break()

# ==================== 第一章 项目概述 ====================
doc.add_heading('第一章  项目概述', level=1)

doc.add_heading('1.1 什么是 RAG', level=2)
add_body('RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合了检索系统和大语言模型的技术。')
add_body('简单来说：大模型本身的知识是固定的（训练时的数据），但 RAG 可以让大模型在回答问题前，先去你的文档库里查找相关资料，然后根据这些资料生成答案。这样答案更准确、有依据、可溯源，还能避免大模型"胡说八道"。')
add_callout('生活类比：就像开卷考试，先从课本里找到相关的几页（检索），然后根据这些内容写答案（生成）。')

doc.add_heading('1.2 项目目标', level=2)
add_body('从零搭建一个完整的 RAG 知识库系统，具备以下能力：')
add_body('① 支持 PDF / Word / TXT 三种格式的文档上传')
add_body('② 自动完成文档加载、文本切片、向量化、存入向量数据库')
add_body('③ 用户提问时，自动检索相关文档片段，由大模型生成答案')
add_body('④ 答案附带来源溯源，知道答案来自哪篇文档的哪个片段')
add_body('⑤ 提供 RESTful API 接口和 Web 前端页面')
add_body('⑥ 支持 Docker 一键部署')

doc.add_heading('1.3 技术栈', level=2)
add_table(
    ['技术', '用途', '说明'],
    [
        ['Python', '开发语言', '3.10+'],
        ['sentence-transformers', '本地向量化', 'bge-small-zh-v1.5 模型，512维，免费无需API'],
        ['DeepSeek API', '大模型对话', 'deepseek-chat 模型，生成答案'],
        ['Chroma', '向量数据库', '轻量级，适合学习和原型开发'],
        ['pypdf', 'PDF 解析', '读取 PDF 文件内容'],
        ['python-docx', 'Word 解析', '读取 Word 文件内容'],
        ['FastAPI', 'API 框架', '提供 HTTP 接口，自动生成接口文档'],
        ['HTML/CSS/JS', '前端页面', '纯原生，无需框架'],
        ['Docker', '部署', '容器化部署（可选）'],
    ],
    col_widths=[3.5, 3.5, 8]
)

doc.add_heading('1.4 RAG 工作流程', level=2)
add_body('整个系统分为两个阶段：')
add_body('【文档入库阶段】加载文档 → 文本切片 → 向量化 → 存入向量数据库')
add_body('【用户提问阶段】问题向量化 → 检索相关片段 → 大模型生成答案 → 返回答案+来源')

# ==================== 第二章 环境准备 ====================
doc.add_heading('第二章  环境准备', level=1)

doc.add_heading('2.1 安装 Python', level=2)
add_body('从 https://www.python.org/downloads/ 下载 Python 3.10+，安装时勾选 "Add Python to PATH"。')
add_body('验证安装：打开 CMD，运行 python --version，能看到版本号即可。')

doc.add_heading('2.2 安装依赖库', level=2)
add_body('在项目根目录下创建 requirements.txt，内容如下：')
add_code('''# 向量数据库
chromadb>=0.4.0

# 文档处理
pypdf>=3.17.0
python-docx>=1.1.0

# 本地向量化模型
sentence-transformers>=2.2.0

# 大模型 API
openai>=1.0.0

# 后端 API
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6

# 工具
numpy>=1.24.0''')
add_body('然后运行：pip install -r requirements.txt')
add_callout('注意：sentence-transformers 会自动安装 PyTorch（约2GB），第一次安装需要一些时间。如果下载慢，可以用国内镜像：pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/simple/')

doc.add_heading('2.3 申请 DeepSeek API Key', level=2)
add_body('1. 打开 https://platform.deepseek.com/')
add_body('2. 注册/登录账号')
add_body('3. 进入 "API Keys" 页面，创建新的 API Key')
add_body('4. 复制保存好你的 API Key（格式类似 sk-xxxxxxxx）')
add_callout('DeepSeek 新用户通常有免费额度，对话价格很便宜，几块钱够用很久。')

doc.add_heading('2.4 本地向量化模型说明', level=2)
add_body('本项目使用 BAAI/bge-small-zh-v1.5 作为向量化模型，这是一个开源的中文轻量模型：')
add_body('• 模型大小：约 100MB')
add_body('• 向量维度：512 维')
add_body('• 完全免费，不需要 API Key')
add_body('• 第一次运行时会自动从 HuggingFace 下载，以后离线可用')
add_callout('如果 HuggingFace 下载慢，可以设置环境变量 HF_ENDPOINT=https://hf-mirror.com 使用国内镜像，或者开启代理。')

# ==================== 第三章 项目结构 ====================
doc.add_heading('第三章  项目结构', level=1)

doc.add_heading('3.1 完整目录树', level=2)
add_code('''rag-project/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py              # FastAPI 接口主程序
│   ├── embedding/
│   │   ├── __init__.py
│   │   └── embedding_service.py # 向量化服务（本地模型）
│   ├── generator/
│   │   ├── __init__.py
│   │   └── llm_generator.py     # 大模型生成器（DeepSeek）
│   ├── loader/
│   │   ├── __init__.py
│   │   ├── txt_loader.py        # TXT 加载器
│   │   ├── pdf_loader.py        # PDF 加载器
│   │   ├── docx_loader.py       # Word 加载器
│   │   └── factory.py           # 工厂类（自动选择加载器）
│   ├── retriever/
│   │   ├── __init__.py
│   │   └── vector_store.py      # 向量数据库（Chroma）
│   ├── splitter/
│   │   ├── __init__.py
│   │   ├── character_splitter.py    # 按字符切片
│   │   └── recursive_splitter.py    # 递归语义切片
│   ├── static/
│   │   └── index.html           # 前端页面
│   ├── __init__.py
│   └── rag_pipeline.py          # RAG 主流程（整合所有模块）
├── data/                        # 测试文档目录
├── chroma_db/                   # 向量数据库存储目录（自动生成）
├── Dockerfile                   # Docker 镜像构建
├── docker-compose.yml           # Docker Compose 配置
├── requirements.txt             # 依赖列表
├── .gitignore                   # Git 忽略文件
└── README.md                    # 项目说明''')

doc.add_heading('3.2 各模块作用', level=2)
add_table(
    ['模块', '作用', '核心文件'],
    [
        ['loader', '读取各种格式的文档，转成纯文本', 'txt_loader.py, pdf_loader.py, docx_loader.py, factory.py'],
        ['splitter', '把长文本切成小块，方便检索和向量化', 'character_splitter.py, recursive_splitter.py'],
        ['embedding', '把文本转换成向量（一串数字）', 'embedding_service.py'],
        ['retriever', '存储向量，支持相似度搜索', 'vector_store.py'],
        ['generator', '把检索结果和问题传给大模型，生成答案', 'llm_generator.py'],
        ['pipeline', '把上面五个模块串起来，形成完整流程', 'rag_pipeline.py'],
        ['api', 'FastAPI 接口封装，提供 HTTP 服务', 'main.py'],
        ['static', '前端页面，用户可视化操作', 'index.html'],
    ],
    col_widths=[2.5, 6, 6.5]
)

# ==================== 第四章 loader ====================
doc.add_heading('第四章  模块一：文档加载器（loader）', level=1)

doc.add_heading('4.1 模块作用', level=2)
add_body('负责读取不同格式的文档文件，统一转换成纯文本字符串。支持 TXT、PDF、Word 三种格式。')

doc.add_heading('4.2 txt_loader.py — TXT 加载器', level=2)
add_body('作用：读取 .txt 文本文件。')
add_code('''class TxtLoader:
    """TXT 文件加载器"""

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self) -> str:
        """加载文件，返回文本内容"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()''')
add_table(
    ['代码', '解释'],
    [
        ['class TxtLoader:', '定义一个类，叫 TxtLoader（TXT加载器）'],
        ['def __init__(self, file_path):', '初始化方法，创建对象时传入文件路径'],
        ['self.file_path = file_path', '把路径存到对象自己身上，后面用'],
        ['def load(self) -> str:', '定义 load 方法，返回字符串'],
        ['with open(...) as f:', '打开文件（with 语句会自动关闭文件）'],
        ['encoding="utf-8"', '指定 UTF-8 编码，避免中文乱码'],
        ['return f.read()', '读取文件全部内容并返回'],
    ],
    col_widths=[5.5, 9.5]
)

doc.add_heading('4.3 pdf_loader.py — PDF 加载器', level=2)
add_body('作用：读取 .pdf 文件，提取每一页的文字内容。')
add_code('''from pypdf import PdfReader

class PDFLoader:
    """PDF 文件加载器"""

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self) -> str:
        reader = PdfReader(self.file_path)
        all_text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                all_text.append(page_text)
        return "\\n".join(all_text)''')
add_table(
    ['代码', '解释'],
    [
        ['from pypdf import PdfReader', '导入 pypdf 库的 PDF 读取器'],
        ['reader = PdfReader(path)', '打开 PDF 文件，创建读取器对象'],
        ['for page in reader.pages:', '遍历 PDF 的每一页'],
        ['page.extract_text()', '提取当前页的文字内容'],
        ['all_text.append(page_text)', '把这一页的文字加到列表'],
        ['"\\n".join(all_text)', '用换行符把所有页的文字连起来'],
    ],
    col_widths=[5.5, 9.5]
)
add_callout('注意：pypdf 只能提取文字型 PDF，扫描件（图片型 PDF）需要 OCR 识别，本项目暂不支持。')

doc.add_heading('4.4 docx_loader.py — Word 加载器', level=2)
add_body('作用：读取 .docx Word 文件，提取所有段落文字。')
add_code('''from docx import Document

class DocxLoader:
    """Word 文件加载器"""

    def __init__(self, file_path):
        self.file_path = file_path

    def load(self) -> str:
        doc = Document(self.file_path)
        all_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                all_text.append(para.text)
        return "\\n".join(all_text)''')

doc.add_heading('4.5 factory.py — 工厂类', level=2)
add_body('作用：根据文件后缀自动选择对应的加载器，调用方不需要关心具体用哪个加载器。')
add_code('''import os
from .txt_loader import TxtLoader
from .pdf_loader import PDFLoader
from .docx_loader import DocxLoader

def get_loader(file_path):
    """根据文件后缀自动选择加载器"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return TxtLoader(file_path)
    elif ext == '.pdf':
        return PDFLoader(file_path)
    elif ext == '.docx':
        return DocxLoader(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")''')
add_body('使用方式：loader = get_loader("test.pdf")，text = loader.load()')

# ==================== 第五章 splitter ====================
doc.add_heading('第五章  模块二：文本切片器（splitter）', level=1)

doc.add_heading('5.1 模块作用', level=2)
add_body('为什么要切片？因为整篇文档可能很长，直接向量化会丢失细节，检索时也不够精准。把长文档切成小块，每块单独向量化，检索时能找到最相关的片段。')

doc.add_heading('5.2 character_splitter.py — 按字符切片', level=2)
add_body('最简单的切片方式：按固定字符数切割，相邻块有重叠，防止句子被切断。')
add_code('''class CharacterSplitter:
    """按字符切片器"""

    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text):
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start = end - self.chunk_overlap
        return chunks''')
add_table(
    ['代码', '解释'],
    [
        ['chunk_size=500', '每块500个字符'],
        ['chunk_overlap=50', '相邻块重叠50个字符，防止句子被切断'],
        ['while start < len(text):', '从开头一直切到结尾'],
        ['text[start:end]', 'Python 切片语法，取出从start到end的文字'],
        ['start = end - overlap', '下一块往前退50个字符，保证重叠'],
    ],
    col_widths=[5.5, 9.5]
)

doc.add_heading('5.3 recursive_splitter.py — 递归语义切片', level=2)
add_body('更智能的切片方式：优先按段落、句子、标点来切，尽量保持语义完整。只有当一块还是太长时，才用更小的分隔符继续切。')
add_code('''class RecursiveSplitter:
    """递归切片器"""

    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # 分隔符优先级：段落 > 换行 > 句号 > 逗号 > 空格
        self.separators = ["\\n\\n", "\\n", "。", "！", "？", ".", "，", " ", ""]

    def split(self, text):
        return self._split_text(text, self.separators)

    def _split_text(self, text, separators):
        # 找到合适的分隔符，递归切分
        # ...（具体实现见源码）
        pass''')
add_callout('项目中默认使用 RecursiveSplitter，因为它能更好地保持语义完整。')

# ==================== 第六章 embedding ====================
doc.add_heading('第六章  模块三：向量化（embedding）', level=1)

doc.add_heading('6.1 模块作用', level=2)
add_body('把文本转换成向量（一串数字）。意思相近的文字，向量也相近；意思不相关的文字，向量距离远。这样就可以通过计算向量相似度来找到相关文档。')
add_callout('生活类比：给每段文字发一个"身份证号"，意思相近的文字，身份证号也相近。搜索时，找到身份证号最接近的那段，就是意思最相关的。')

doc.add_heading('6.2 embedding_service.py — 向量化服务', level=2)
add_body('使用本地开源模型 BAAI/bge-small-zh-v1.5，完全免费，不需要 API Key。')
add_code('''from sentence_transformers import SentenceTransformer

class EmbeddingService:
    """向量化服务（本地模型版）"""

    def __init__(self, model_name="BAAI/bge-small-zh-v1.5"):
        print(f"正在加载本地向量化模型: {model_name} ...")
        self.model = SentenceTransformer(model_name)
        print("模型加载完成！")

    def embed(self, text: str) -> list:
        """把单条文本转换成向量"""
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: list) -> list:
        """批量把多条文本转换成向量"""
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vectors]''')
add_table(
    ['代码', '解释'],
    [
        ['SentenceTransformer(model_name)', '加载本地向量化模型，第一次运行自动下载'],
        ['model.encode(text)', '把文本编码成向量'],
        ['normalize_embeddings=True', '归一化向量，方便计算余弦相似度'],
        ['vector.tolist()', '把 numpy 数组转成 Python 列表，方便存储和传输'],
        ['embed_batch', '批量向量化，一次传多条文本，比一条条调更高效'],
    ],
    col_widths=[5.5, 9.5]
)
add_callout('模型下载：第一次运行会从 HuggingFace 下载约100MB的模型文件。如果下载慢，设置环境变量 HF_ENDPOINT=https://hf-mirror.com 使用国内镜像。')

doc.add_heading('6.3 相似度验证', level=2)
add_body('可以用以下代码验证向量化效果：')
add_code('''import numpy as np

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

service = EmbeddingService()
texts = ["我喜欢Python", "我喜欢Java", "今天天气真好"]
vectors = service.embed_batch(texts)

v1, v2, v3 = [np.array(v) for v in vectors]
print(f"Python vs Java 相似度: {cosine_sim(v1, v2):.4f}")  # 约0.85，意思相近
print(f"Python vs 天气 相似度: {cosine_sim(v1, v3):.4f}")  # 约0.35，意思不相关''')

# ==================== 第七章 retriever ====================
doc.add_heading('第七章  模块四：向量数据库（retriever）', level=1)

doc.add_heading('7.1 模块作用', level=2)
add_body('存储文档向量，支持相似度搜索。用户提问时，把问题也转成向量，然后在数据库里找到最相似的几个文档片段。')

doc.add_heading('7.2 vector_store.py — 向量存储与检索', level=2)
add_body('使用 Chroma 作为向量数据库，轻量级，数据持久化到本地文件夹。')
add_code('''import chromadb

class VectorStore:
    """向量数据库"""

    def __init__(self, collection_name="rag_knowledge_base", persist_directory="./chroma_db"):
        # 创建客户端，数据会保存到本地
        self.client = chromadb.PersistentClient(path=persist_directory)
        # 创建集合（类似数据库里的表）
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # 用余弦相似度
        )

    def add_documents(self, documents, embeddings, metadatas=None, ids=None):
        """添加文档和向量到数据库"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        if metadatas is None:
            metadatas = [{"source": "unknown"} for _ in range(len(documents))]
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query_embedding, top_k=5):
        """搜索最相似的文档"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        output = []
        for i in range(len(results['documents'][0])):
            output.append({
                'document': results['documents'][0][i],
                'distance': results['distances'][0][i],
                'metadata': results['metadatas'][0][i],
                'id': results['ids'][0][i]
            })
        return output

    def count(self):
        """返回数据库中的文档数量"""
        return self.collection.count()

    def clear(self):
        """清空集合"""
        name = self.collection.name
        self.client.delete_collection(name)
        self.collection = self.client.get_or_create_collection(
            name=name, metadata={"hnsw:space": "cosine"}
        )''')
add_table(
    ['代码', '解释'],
    [
        ['chromadb.PersistentClient(path=...)', '创建客户端，数据持久化到本地文件夹，下次打开还在'],
        ['get_or_create_collection(...)', '创建集合（类似表），不存在就创建，存在就获取'],
        ['metadata={"hnsw:space": "cosine"}', '指定用余弦相似度计算'],
        ['collection.add(...)', '添加文档、向量、元数据、ID到集合'],
        ['collection.query(...)', '搜索，传入查询向量，返回最相似的top_k条'],
        ["results['distances'][0][i]", '距离，越小越相似（用1-distance转成相似度）'],
        ['clear()', '删除整个集合再重建，实现清空'],
    ],
    col_widths=[5.5, 9.5]
)

# ==================== 第八章 generator ====================
doc.add_heading('第八章  模块五：LLM 生成器（generator）', level=1)

doc.add_heading('8.1 模块作用', level=2)
add_body('把检索到的相关文档片段和用户问题一起传给大模型，让大模型基于这些资料生成答案。同时附带来源信息。')

doc.add_heading('8.2 llm_generator.py — 大模型生成器', level=2)
add_body('使用 DeepSeek API（deepseek-chat 模型）。')
add_code('''from openai import OpenAI

class LLMGenerator:
    """大模型生成器（DeepSeek版）"""

    def __init__(self, api_key, base_url="https://api.deepseek.com", model="deepseek-chat"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def generate(self, question, context):
        """根据问题和上下文生成答案"""
        prompt = f"""你是一个专业的问答助手。请根据下面提供的参考资料回答用户的问题。

【参考资料】
{context}

【用户问题】
{question}

【回答要求】
1. 只根据参考资料中的内容回答，不要编造资料中没有的信息
2. 如果参考资料中没有相关信息，请回答"根据现有资料无法回答这个问题"
3. 回答要简洁明了，分点说明
4. 答案用中文

请给出你的回答："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content

    def generate_with_sources(self, question, documents):
        """生成答案并附带来源"""
        context_parts = []
        for i, doc in enumerate(documents):
            source = doc.get('metadata', {}).get('source', f'文档{i+1}')
            context_parts.append(f"[来源{i+1}: {source}]\\n{doc['document']}")
        context = "\\n\\n".join(context_parts)

        answer = self.generate(question, context)
        return {
            'question': question,
            'answer': answer,
            'sources': [doc.get('metadata', {}) for doc in documents]
        }''')
add_table(
    ['代码', '解释'],
    [
        ['OpenAI(api_key=..., base_url=...)', '创建客户端，指向 DeepSeek 的API地址（兼容OpenAI格式）'],
        ['model="deepseek-chat"', 'DeepSeek 的对话模型'],
        ['prompt = f"""..."""', '构造提示词，把参考资料和问题组合起来'],
        ['【回答要求】部分', '明确告诉模型回答规则，减少编造'],
        ['temperature=0.3', '温度参数，越低回答越稳定、越确定'],
        ['chat.completions.create(...)', '调用对话API，生成答案'],
        ['generate_with_sources', '在上下文中标注来源，返回答案时附带来源信息'],
    ],
    col_widths=[5.5, 9.5]
)
add_callout('关键技巧：在 prompt 中明确告诉模型"只根据参考资料回答，不要编造"，这样能有效减少大模型"胡说八道"的问题。')

# ==================== 第九章 pipeline ====================
doc.add_heading('第九章  模块六：主流程（pipeline）', level=1)

doc.add_heading('9.1 模块作用', level=2)
add_body('把前面五个模块串起来，形成完整的 RAG 流程。对外提供两个核心方法：ingest（上传文档）和 query（提问）。')

doc.add_heading('9.2 rag_pipeline.py — 完整流程', level=2)
add_code('''from loader.factory import get_loader
from splitter.recursive_splitter import RecursiveSplitter
from embedding.embedding_service import EmbeddingService
from retriever.vector_store import VectorStore
from generator.llm_generator import LLMGenerator

class RAGPipeline:
    """RAG 完整流程"""

    def __init__(self, api_key, persist_directory="./chroma_db"):
        self.embedding_service = EmbeddingService()
        self.splitter = RecursiveSplitter(chunk_size=500, chunk_overlap=50)
        self.vector_store = VectorStore(persist_directory=persist_directory)
        self.generator = LLMGenerator(api_key=api_key)
        print("RAG 系统初始化完成")

    def ingest(self, file_path):
        """上传文档，处理后存入向量数据库"""
        print(f"正在处理文档: {file_path}")

        # 第1步：加载文档
        print("  [1/4] 加载文档...")
        loader = get_loader(file_path)
        text = loader.load()
        print(f"  文档长度: {len(text)} 字符")

        # 第2步：文本切片
        print("  [2/4] 文本切片...")
        chunks = self.splitter.split(text)
        print(f"  切成了 {len(chunks)} 块")

        # 第3步：向量化
        print("  [3/4] 向量化...")
        embeddings = self.embedding_service.embed_batch(chunks)

        # 第4步：存入向量数据库
        print("  [4/4] 存入向量数据库...")
        import os
        metadatas = [{"source": os.path.basename(file_path), "chunk_id": i} for i in range(len(chunks))]
        ids = [f"{os.path.basename(file_path)}_{i}" for i in range(len(chunks))]
        self.vector_store.add_documents(chunks, embeddings, metadatas, ids)

        print(f"  完成！共存入 {len(chunks)} 块")
        return len(chunks)

    def query(self, question, top_k=3):
        """用户提问，检索并生成答案"""
        # 第1步：问题向量化
        question_vec = self.embedding_service.embed(question)

        # 第2步：检索相关文档
        results = self.vector_store.search(question_vec, top_k=top_k)

        # 第3步：生成答案
        result = self.generator.generate_with_sources(question, results)
        return result

    def get_document_count(self):
        """获取数据库中的文档块数量"""
        return self.vector_store.count()''')

doc.add_heading('9.3 流程示意图', level=2)
add_body('【文档入库】文件 → loader加载 → splitter切片 → embedding向量化 → retriever存库')
add_body('【用户提问】问题 → embedding向量化 → retriever检索 → generator生成 → 答案+来源')

# ==================== 第十章 FastAPI ====================
doc.add_heading('第十章  FastAPI 接口封装', level=1)

doc.add_heading('10.1 为什么要做 API', level=2)
add_body('前面的模块都是 Python 代码，只能在 Python 里调用。封装成 API 后，任何程序（前端网页、手机App、其他服务）都可以通过 HTTP 请求调用 RAG 系统。')

doc.add_heading('10.2 接口设计', level=2)
add_table(
    ['接口', '方法', '功能', '参数'],
    [
        ['/', 'GET', '系统状态，返回文档数量', '无'],
        ['/upload', 'POST', '上传文档，自动处理并存库', 'file: 文件'],
        ['/query', 'POST', '提问，返回答案和来源', 'question: 问题, top_k: 数量'],
        ['/documents', 'GET', '获取文档块数量', '无'],
        ['/clear', 'DELETE', '清空向量数据库', '无'],
    ],
    col_widths=[2.5, 2, 5.5, 5]
)

doc.add_heading('10.3 main.py 核心代码', level=2)
add_code('''from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os, sys, tempfile, traceback

# 把 src 目录加到路径
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)
from rag_pipeline import RAGPipeline

app = FastAPI(title="RAG 知识库系统 API", version="1.0.0")

# 允许跨域
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 全局 RAG 系统实例（懒加载）
rag_system = None
API_KEY = "你的DeepSeek_API_Key"
PERSIST_DIR = os.path.join(src_path, "chroma_db")

def get_rag_system():
    global rag_system
    if rag_system is None:
        rag_system = RAGPipeline(api_key=API_KEY, persist_directory=PERSIST_DIR)
    return rag_system

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    tmp_path = None
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        system = get_rag_system()
        chunks_count = system.ingest(tmp_path)
        return {"filename": file.filename, "chunks": chunks_count, "message": "上传成功"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.post("/query")
async def query(request: QueryRequest):
    system = get_rag_system()
    return system.query(request.question, top_k=request.top_k)

# 挂载前端静态文件
static_dir = os.path.join(src_path, "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)''')

doc.add_heading('10.4 启动与测试', level=2)
add_body('启动服务：python src/api/main.py')
add_body('服务启动后：')
add_body('• 访问 http://localhost:8000/ → 前端页面')
add_body('• 访问 http://localhost:8000/docs → 自动生成的接口文档（Swagger UI），可以直接在页面上测试接口')

# ==================== 第十一章 前端 ====================
doc.add_heading('第十一章  前端页面开发', level=1)

doc.add_heading('11.1 页面功能', level=2)
add_body('纯 HTML/CSS/JS 实现，不需要任何框架，单文件即可运行。')
add_table(
    ['区域', '功能'],
    [
        ['左侧边栏', '文档上传（点击/拖拽）、文档数量统计、清空知识库按钮'],
        ['右侧聊天区', '聊天式问答界面，显示答案和参考来源'],
        ['底部输入框', '输入问题，回车或点击发送'],
    ],
    col_widths=[3, 12]
)

doc.add_heading('11.2 核心技术点', level=2)
add_body('• 文件上传：FormData + fetch 调用 /upload 接口')
add_body('• 提问：fetch POST 调用 /query 接口，JSON 格式')
add_body('• 实时显示：动态创建 DOM 元素，显示用户消息和 AI 回复')
add_body('• 加载动画：三个点跳动的 CSS 动画')
add_body('• 来源展示：答案下方显示参考来源（文档名+块ID）')

doc.add_heading('11.3 使用方式', level=2)
add_body('启动 API 服务后，直接访问 http://localhost:8000/ 即可看到前端页面。')
add_body('1. 左侧上传文档（PDF/Word/TXT）')
add_body('2. 等待上传完成')
add_body('3. 右侧输入问题，回车发送')
add_body('4. 查看答案和参考来源')

# ==================== 第十二章 Docker ====================
doc.add_heading('第十二章  Docker 部署', level=1)

doc.add_heading('12.1 Dockerfile', level=2)
add_code('''FROM python:3.10-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \\
    HF_ENDPOINT=https://hf-mirror.com \\
    DEEPSEEK_API_KEY=你的API_Key

RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/simple/

COPY src/ ./src/
RUN mkdir -p /app/data /app/chroma_db
EXPOSE 8000
CMD ["python", "src/api/main.py"]''')

doc.add_heading('12.2 docker-compose.yml', level=2)
add_code('''version: "3.8"
services:
  rag-api:
    build: .
    container_name: rag-knowledge-base
    ports:
      - "8000:8000"
    volumes:
      - ./chroma_db:/app/chroma_db
      - ./data:/app/data
    environment:
      - DEEPSEEK_API_KEY=你的API_Key
      - HF_ENDPOINT=https://hf-mirror.com
    restart: unless-stopped''')

doc.add_heading('12.3 部署命令', level=2)
add_body('构建并启动：docker-compose up -d --build')
add_body('查看日志：docker-compose logs -f')
add_body('停止服务：docker-compose down')
add_callout('注意：Docker 部署需要先安装 Docker Desktop 和 WSL 2。容器内第一次启动会下载向量化模型，需要一些时间。')

# ==================== 第十三章 模型切换 ====================
doc.add_heading('第十三章  模型切换说明', level=1)

doc.add_heading('13.1 为什么切换', level=2)
add_body('项目最初使用智谱 GLM 的 API（embedding-3 向量化 + glm-4-flash 对话），但智谱最低充值100元，对于学习项目成本较高。因此切换为：')
add_body('• 向量化：本地开源模型 bge-small-zh-v1.5（完全免费）')
add_body('• 对话：DeepSeek API（价格便宜，新用户有免费额度）')

doc.add_heading('13.2 向量化切换对比', level=2)
add_table(
    ['对比项', '智谱 embedding-3', '本地 bge-small-zh'],
    [
        ['是否需要API', '是', '否'],
        ['费用', '按调用量收费', '完全免费'],
        ['向量维度', '2048维', '512维'],
        ['是否需要联网', '是', '否（第一次下载后离线可用）'],
        ['中文效果', '好', '良好（足够学习和原型使用）'],
        ['首次使用', '直接调用', '需下载约100MB模型'],
    ],
    col_widths=[3, 6, 6]
)

doc.add_heading('13.3 对话切换对比', level=2)
add_table(
    ['对比项', '智谱 glm-4-flash', 'DeepSeek deepseek-chat'],
    [
        ['API地址', 'https://open.bigmodel.cn/api/paas/v4/', 'https://api.deepseek.com'],
        ['最低充值', '100元', '无最低限制'],
        ['价格', '免费额度后收费', '便宜，新用户有免费额度'],
        ['代码改动', '—', '只需改 base_url 和 model 名'],
    ],
    col_widths=[3, 6, 6]
)

doc.add_heading('13.4 切换注意事项', level=2)
add_body('① 向量化模型切换后，向量维度从2048变成512，旧的向量数据库不能用了，需要删除 chroma_db 目录重新生成。')
add_body('② 本地模型第一次运行会自动下载，确保网络通畅，或设置 HF_ENDPOINT 环境变量用国内镜像。')
add_body('③ DeepSeek API 兼容 OpenAI 格式，所以代码里还是用 openai 库，只需要改 base_url 和 model 名。')

# ==================== 第十四章 完整复现步骤 ====================
doc.add_heading('第十四章  从0到1完整复现步骤', level=1)

steps = [
    ('第一步：创建项目结构', '创建 rag-project 目录，按第三章的目录树创建所有文件夹和 __init__.py 文件。'),
    ('第二步：实现文档加载器', '依次编写 txt_loader.py、pdf_loader.py、docx_loader.py、factory.py，每个都写测试代码验证。'),
    ('第三步：实现文本切片器', '编写 character_splitter.py 和 recursive_splitter.py，测试切片效果。'),
    ('第四步：实现向量化服务', '安装 sentence-transformers，编写 embedding_service.py，第一次运行会自动下载模型。测试相似度。'),
    ('第五步：实现向量数据库', '安装 chromadb，编写 vector_store.py，测试添加和搜索。'),
    ('第六步：实现 LLM 生成器', '申请 DeepSeek API Key，编写 llm_generator.py，测试对话生成。'),
    ('第七步：串联主流程', '编写 rag_pipeline.py，整合五个模块，测试完整的 ingest 和 query 流程。'),
    ('第八步：FastAPI 接口封装', '安装 fastapi、uvicorn、python-multipart，编写 api/main.py，启动服务并用 Swagger UI 测试。'),
    ('第九步：前端页面', '编写 static/index.html，实现上传和聊天界面，测试完整交互。'),
    ('第十步：Docker 部署（可选）', '编写 Dockerfile 和 docker-compose.yml，安装 Docker 后一键部署。'),
    ('第十一步：提交到 GitHub', '创建 GitHub 仓库，编写 .gitignore，提交所有代码。'),
]
for i, (title, desc) in enumerate(steps, 1):
    doc.add_heading(f'14.{i} {title}', level=3)
    add_body(desc)

# ==================== 第十五章 常见问题 ====================
doc.add_heading('第十五章  常见问题与解决方案', level=1)

add_table(
    ['问题', '原因', '解决方案'],
    [
        ['ModuleNotFoundError: No module named xxx', '依赖没装或Python环境不对', 'pip install xxx；确认用的是同一个Python环境（where python）'],
        ['API 报错 401', 'API Key 错误或过期', '检查 Key 是否正确，重新生成'],
        ['API 报错 429 余额不足', 'API 额度用完了', '充值或换其他API；向量化可换成本地模型'],
        ['向量化模型下载慢/超时', 'HuggingFace国内访问不稳定', '设置 HF_ENDPOINT=https://hf-mirror.com 或开启代理'],
        ['上传文档返回500', '处理过程中出错', '看CMD窗口的完整错误堆栈；常见原因：API余额不足、文件格式不对'],
        ['Chroma delete 报错', '不支持空条件删除', '用 delete_collection 删整个集合再重建'],
        ['PDF 提取文字为空', 'PDF 是扫描件（图片）', '需要 OCR 识别，本项目暂不支持扫描件'],
        ['中文显示乱码', '编码问题', 'open 文件时指定 encoding="utf-8"'],
        ['Docker 启动失败 虚拟化未检测到', 'BIOS 虚拟化未开启或WSL未安装', 'BIOS开启VT-x；安装WSL 2；或暂时跳过Docker'],
        ['向量数据库报错 维度不匹配', '换了向量化模型后维度变了', '删除旧的 chroma_db 目录，重新生成'],
    ],
    col_widths=[4, 4, 7]
)

# ==================== 第十六章 简历描述 ====================
doc.add_heading('第十六章  简历描述参考', level=1)

doc.add_heading('16.1 项目名称', level=2)
add_body('RAG 知识库系统 / 智能文档问答系统')

doc.add_heading('16.2 项目描述（简历用）', level=2)
add_body('独立设计并实现基于检索增强生成（RAG）的智能知识库系统，支持 PDF/Word/TXT 多格式文档上传与智能问答。')
add_body('• 采用模块化架构，实现文档加载、文本切片、向量化、向量检索、大模型生成六大核心模块')
add_body('• 基于本地 bge-small-zh 开源模型实现文本向量化（512维），结合 Chroma 向量数据库实现语义检索')
add_body('• 集成 DeepSeek 大模型 API，基于检索上下文生成答案并支持来源溯源，有效减少幻觉')
add_body('• 使用 FastAPI 封装 RESTful 接口，提供文档上传、智能问答、知识库管理等5个API')
add_body('• 开发纯原生 HTML/CSS/JS 前端页面，支持拖拽上传和聊天式问答交互')
add_body('• 编写 Dockerfile 和 docker-compose.yml，支持容器化一键部署')

doc.add_heading('16.3 技术栈关键词', level=2)
add_body('Python、RAG、语义检索、向量数据库、Chroma、sentence-transformers、FastAPI、DeepSeek、Docker、RESTful API')

doc.add_heading('16.4 面试可能问到的问题', level=2)
add_body('1. RAG 的工作流程是什么？为什么需要 RAG？')
add_body('2. 文本切片为什么要重叠？chunk_size 怎么选？')
add_body('3. 向量相似度有哪些计算方式？余弦相似度的原理？')
add_body('4. 怎么减少大模型幻觉？你的项目怎么做的？')
add_body('5. Chroma 和 Milvus、FAISS 的区别？')
add_body('6. 你的系统怎么评估效果？')
add_body('7. 如果文档很多，检索慢怎么办？')
add_body('8. 本地模型和 API 模型的优缺点？')

# ==================== 结尾 ====================
doc.add_page_break()
end = doc.add_paragraph()
end.alignment = WD_ALIGN_PARAGRAPH.CENTER
end.paragraph_format.space_before = Pt(100)
run = end.add_run('—— 文档结束 ——')
run.font.name = '微软雅黑'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

# 保存
output_path = r'D:\AI_Agent三个项目初始结构\rag-project\RAG知识库系统搭建全过程详解_完整更新版.docx'
doc.save(output_path)
print(f'文档已生成: {output_path}')
print(f'文件大小: {__import__("os").path.getsize(output_path)} bytes')
