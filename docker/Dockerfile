# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 必要なPythonパッケージをインストール
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY src/ .

# 環境変数を設定
ENV PYTHONUNBUFFERED=1

# Streamlitのポートを開放
EXPOSE 8501

# アプリケーションを実行
CMD ["streamlit", "run", "main.py"] 
