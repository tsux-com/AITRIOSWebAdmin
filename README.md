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
    - Dockerfile
- server/
    - webapp.py
    - image/
    - meta/
    - Dockerfile
- .env
- docker-compose.yml

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

```
{
    "commands": [
      {
        "command_name": "StartUploadInferenceData",
        "parameters": {
          "Mode": 1,
          "UploadMethod": "HTTPStorage",
          "StorageName": "ここに実際のIPアドレス (例: "192.168.x.x") を入力",
          "StorageSubDirectoryPath": "/image",
          "FileFormat": "JPG",
          "UploadMethodIR": "HTTPStorage",
          "StorageNameIR": "ここに実際のIPアドレス (例: "192.168.x.x") を入力",
          "StorageSubDirectoryPathIR": "/meta",
          "PPLParameter": {
            "header" :{
                "id" : "00",
                "version" : "01.01.00"
            },
            "dnn_output_detections" : 64,
            "max_detections" : 1,
            "threshold" : 0.3,
            "input_width" : 320,
            "input_height" : 320
          },
          "NumberOfImages": 0,
          "UploadInterval": 30,
          "NumberOfInferencesPerMessage": 1
        }
      }
    ]
}
```

---

## 実行コマンド

pip install を行ってください。
web フォルダ及び server フォルダに各 requirements.txt を配置しています

```

pip install -r requirements.txt

```

### HTTP Server 　の立ち上げ ：

```

uvicorn webapp:app_ins --reload --host 192.168.0.23 --port 8080 --no-access-log

```

### web アプリ　の立ち上げ ：

#### 仮想環境作成

web 直下に移動後、以下のコマンドを実行します

```
python -m venv venv
```

#### 仮想環境のアクティベート

Linux, Mac の場合

```
. venv/bin/activate
```

Windows の場合

```
.\venv\Scripts\Activate
```

#### web アプリの立ち上げ

上記の仮想環境がアクティベートになってから下記を実行

```

uvicorn app:app --reload --port 8000

```

---

## Docker 実行

上記の Python を実行するのではなく Docker 上で起動することが可能です

プロジェクトのルートディレクトリ（web/server の両方があり docker-compose.yml
がある場所）で以下のコマンドを実行して、コンテナをビルド・起動します

両方のコンテナ（server と web）をまとめて管理しており、両方が起動します。

### 実行コマンド

```
docker-compose up --build
```
