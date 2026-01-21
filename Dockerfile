# 使用多階段建置以減少最終映像大小
FROM python:3.11-slim as builder

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴（如果需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 最終階段
FROM python:3.11-slim

WORKDIR /app

# 從 builder 階段複製已安裝的套件
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 複製應用程式代碼
COPY --chown=appuser:appuser . .

# 創建非 root 用戶以提高安全性
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# 切換到非 root 用戶
USER appuser

# 設置環境變數
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 5000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/')" || exit 1

# 運行應用程式
CMD ["python", "app.py"]
