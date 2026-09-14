# RAG 知识库系统 Docker 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
# DEEPSEEK_API_KEY 通过 docker-compose 或运行时 -e 参数传入，不要硬编码
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HF_ENDPOINT=https://hf-mirror.com

# 安装系统依赖（torch 和 sentence-transformers 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件，利用 Docker 缓存
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/simple/

# 复制项目代码
COPY src/ ./src/

# 创建数据目录
RUN mkdir -p /app/data /app/chroma_db

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "src/api/main.py"]
