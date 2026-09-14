"""
RAG 系统 API 接口
基于 FastAPI，提供文档上传和问答接口
"""

import os
import sys
import tempfile
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 从 .env 文件加载环境变量（如果安装了 python-dotenv）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 把 src 目录加到路径
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from rag_pipeline import RAGPipeline

# 初始化 FastAPI 应用
app = FastAPI(
    title="RAG 知识库系统 API",
    description="支持文档上传和智能问答的检索增强生成系统",
    version="1.0.0"
)

# 允许跨域（前端调用需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局 RAG 系统实例（懒加载，第一次调用时初始化）
rag_system = None
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
PERSIST_DIR = os.path.join(src_path, "chroma_db")

if not API_KEY:
    print("警告：未设置 DEEPSEEK_API_KEY 环境变量，请在 .env 文件中配置")


def get_rag_system():
    """获取或初始化 RAG 系统"""
    global rag_system
    if rag_system is None:
        rag_system = RAGPipeline(api_key=API_KEY, persist_directory=PERSIST_DIR)
    return rag_system


# 请求模型
class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


# 响应模型
class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list


class UploadResponse(BaseModel):
    filename: str
    chunks: int
    message: str


class StatusResponse(BaseModel):
    document_count: int
    status: str


@app.get("/status", response_model=StatusResponse)
async def root():
    """系统状态"""
    system = get_rag_system()
    return {
        "document_count": system.get_document_count(),
        "status": "running"
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    上传文档，自动处理并存入向量数据库
    支持 .txt / .pdf / .docx
    """
    # 检查文件格式
    allowed_extensions = {'.txt', '.pdf', '.docx'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"不支持的文件格式: {ext}，支持 {allowed_extensions}")

    # 保存上传的文件到临时目录
    tmp_path = None
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        # 处理文档
        system = get_rag_system()
        chunks_count = system.ingest(tmp_path)

        return {
            "filename": file.filename,
            "chunks": chunks_count,
            "message": f"文档上传成功，切成 {chunks_count} 块并存入数据库"
        }
    except Exception as e:
        print("=" * 60)
        print("【上传文档出错】")
        traceback.print_exc()
        print("=" * 60)
        raise HTTPException(status_code=500, detail=f"处理文档失败: {str(e)}")
    finally:
        # 确保临时文件被删除
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except:
                pass


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    提问接口，基于知识库内容生成答案
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    try:
        system = get_rag_system()
        result = system.query(request.question, top_k=request.top_k)
        return result
    except Exception as e:
        print("=" * 60)
        print("【提问出错】")
        traceback.print_exc()
        print("=" * 60)
        raise HTTPException(status_code=500, detail=f"生成答案失败: {str(e)}")


@app.get("/documents")
async def get_document_count():
    """获取数据库中的文档块数量"""
    system = get_rag_system()
    return {"count": system.get_document_count()}


@app.delete("/clear")
async def clear_database():
    """清空向量数据库"""
    system = get_rag_system()
    system.vector_store.clear()
    return {"message": "数据库已清空"}


# 挂载前端静态文件（必须放在所有 API 路由之后）
static_dir = os.path.join(src_path, "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
