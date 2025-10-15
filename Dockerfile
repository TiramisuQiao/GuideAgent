# 米塔视界销售策略AI代理 - Docker部署配置

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装uv包管理器
RUN pip install uv

# 复制项目文件
COPY pyproject.toml .
COPY requirements.txt .
COPY sales_agent.py .
COPY web_app.py .
COPY example_usage.py .
COPY .env.example .

# 使用uv安装依赖
RUN uv pip install --system -r requirements.txt

# 暴露Streamlit默认端口
EXPOSE 8501

# 设置环境变量
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 启动命令
CMD ["streamlit", "run", "web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
