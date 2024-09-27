# Python 3.11 slim イメージを使用
FROM python:3.11-slim

# 作業ディレクトリを作成
WORKDIR /app

# requirements.txt を最初にコピーして依存関係をインストール
COPY requirements.txt /app/

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ローカルファイルをコンテナにコピー
COPY . /app

# 必要なポートを公開
EXPOSE 8000

# サーバー起動コマンド
CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]