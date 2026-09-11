# RAG 知识库系统

> 生产级检索增强生成（Retrieval-Augmented Generation）系统，支持文档上传、智能切片、向量检索、多轮问答。

## 项目简介

本项目实现了一个完整的 RAG 知识库系统，覆盖从文档摄入到问答生成的全流程，是 AI Agent 工程师岗位的核心项目之一。

## 技术栈

- **框架**: LangChain / LlamaIndex
- **大模型**: OpenAI / 通义千问 / 智谱 GLM
- **向量数据库**: Milvus / Chroma / FAISS
- **文档处理**: PyPDF / python-docx / Unstructured
- **Embedding**: text-embedding-ada-002 / BGE
- **后端**: FastAPI
- **部署**: Docker

## 功能特性

- [ ] 多格式文档解析（PDF / Word / Markdown / TXT）
- [ ] 智能文本切片（按语义 / 按字符 / 递归）
- [ ] 向量存储与检索（支持相似度 + 重排序）
- [ ] 多轮对话问答（带历史上下文）
- [ ] 引用溯源（答案标注来源段落）
- [ ] RESTful API 接口
- [ ] Docker 一键部署

## 目录结构

```
rag-project/
├── data/                  # 示例文档
├── src/
│   ├── loader/            # 文档加载器
│   ├── splitter/          # 文本切片器
│   ├── embedding/         # 向量化模块
│   ├── retriever/         # 检索器
│   ├── generator/         # 生成器（LLM 问答）
│   └── api/               # FastAPI 接口
├── config/                # 配置文件
├── tests/                 # 单元测试
├── docs/                  # 文档
├── requirements.txt
└── README.md
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp config/.env.example config/.env
# 编辑 config/.env，填入你的 API Key

# 3. 运行服务
python -m src.api.main
```

## 学习路径

1. **Week 1**: 文档加载 + 文本切片
2. **Week 2**: Embedding + 向量数据库
3. **Week 3**: 检索器 + 重排序
4. **Week 4**: LLM 生成 + 多轮对话
5. **Week 5**: API 封装 + Docker 部署

## 简历亮点（完成后可写）

- 独立构建生产级 RAG 知识库系统，支持 PDF/Word/Markdown 等多格式文档
- 实现语义切片 + 混合检索 + Rerank 重排序，召回率提升 XX%
- 基于 LangChain 搭建检索问答链路，支持多轮对话与引用溯源
- 使用 Milvus 向量数据库存储百万级向量，查询延迟 < 200ms
- FastAPI 封装 RESTful 接口，Docker 部署，支持并发 XX QPS
