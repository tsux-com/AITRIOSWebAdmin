# Web アプリケーション仕様書

## 概要

このドキュメントは、FastAPI を使用した Web アプリケーションの仕様書です。

WEB アプリ　管理画面を介して外部 API を呼び出し、デバイスの推論開始および停止する機能。

---

## アプリケーション構成

```
- web/
    - app.py
    - access_token.py
    - api_services/
        - service.py
    - templates/
        - index.html
- server/
    - webapp.py
    - image/
    - meta/
- .env
```

---

## 各スクリプトの詳細

### 1. server/webapp.py

このスクリプトは、FastAPI を使用して、メタデータファイルと画像ファイルをアップロードし、指定されたパスに保存するための API を提供します。

- **機能**:
  - 画像ファイルおよびメタデータファイルの保存
  - リクエストのロギング

#### 詳細説明

- **ログの設定**: すべての HTTP リクエストを記録するためのミドルウェアを追加。
- **メタデータの保存**: `PUT /meta/{filename}` エンドポイントを使用してメタデータを保存。
- **画像の保存**: `PUT /image/{filename}` エンドポイントを使用して画像を保存。

---

### 2. web/app.py

このスクリプトは、ユーザーが API を開始・停止するための UI を提供します。Jinja2 テンプレートを使用して HTML をレンダリングし、API 呼び出しを行う。

- **機能**:
  - HTML テンプレートのレンダリング
  - API 開始・停止操作

#### 詳細説明

- **トークン管理**: 各 API 呼び出し時に、`load_access_token()` を使用してトークンをロード。
- **API 呼び出し**: ユーザーがボタンをクリックすると、外部 API に対してデバイスのデータ収集開始または停止リクエストが送信される。

---

### 3. web/access_token.py

このスクリプトは、外部 API へのアクセスに必要なトークンを取得し、管理します。

トークンは一度取得するとテキストファイル( access_token.txt )に保存され、必要に応じて再利用されます。

- **機能**:
  - OAuth2 クライアント認証によるアクセストークンの取得
  - トークンの有効期限の管理と再取得

#### 詳細説明

- **トークン取得**: `get_access_token()` 関数を使用して、外部 API から新しいトークンを取得。
- **トークンロード**: トークンはファイルからロードされ、有効期限が切れている場合は再取得される。

---

### 4. api_services/service.py

推論開始・停止するために外部 API に対して POST リクエストを送信します。

- **機能**:
  - 外部 API にデバイスのデータ収集開始・停止リクエストを送信
  - API レスポンスの処理

#### 詳細説明

- **API 呼び出し**:
  - `post_collectstart_to_api()` は推論開始リクエストを送信。
  - `post_collectstop_to_api()` は推論停止リクエストを送信。
- **エラーハンドリング**: リクエスト失敗時や無効な JSON レスポンス時には適切なエラーメッセージを返却。

---

## 環境変数 (`.env` ファイル)

クライアント ID とクライアントシークレットを環境変数として管理しています。

`.env` ファイルから以下の環境変数が読み込まれます。

- `CLIENT_ID`: クライアント ID
- `CLIENT_SECRET`: クライアントシークレット

---

## テンプレートファイル (`index.html`)

HTML ファイルは、Jinja2 テンプレートを使用してレンダリングされ、API 呼び出しを行うためのボタンが配置されています。

---

## command parameter

HTTPStorageSample.json にてサンプルを確認ください

"StorageName": ここに実際の IP アドレス (例: "192.168.x.x") を入力

"StorageNameIR": ここに実際の IP アドレス (例: "192.168.x.x") を入力

---

## 実行コマンド

pip install を行ってください。
web フォルダ及び server フォルダに各 requirements.txt を配置しています

```

pip install -r requirements.txt

```

HTTP Server 　の立ち上げ ：

```

uvicorn webapp:app_ins --reload --host 192.168.0.23 --port 8080 --no-access-log

```

web アプリ　の立ち上げ ：

```

.\venv\Scripts\Activate

```

```

uvicorn "app:app --reload --port 8000"

```
