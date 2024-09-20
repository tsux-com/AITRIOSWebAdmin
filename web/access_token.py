import requests
import base64
import json
import time
from dotenv import load_dotenv
import os

# .envファイルの内容を読み込む
load_dotenv()

# デバッグ用にプリント文を追加
print("スクリプトが開始されました")

# クライアントIDとシークレットをBase64エンコード
client_id = os.getenv("CLIENT_ID") #your_client_id_here
client_secret = os.getenv("CLIENT_SECRET") #your_client_secret_here

client_credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(client_credentials.encode("utf-8")).decode("utf-8")

def get_access_token():
    url = "https://auth.aitrios.sony-semicon.com/oauth2/default/v1/token"
    
    # デバッグ用にプリント文を追加
    print("アクセストークンを取得中...")

    # ヘッダーの設定
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {encoded_credentials}",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded"
    }
    
    # データ（POSTリクエストのパラメータ）
    data = {
        "grant_type": "client_credentials",
        "scope": "system"
    }
    
    # POSTリクエストを送信してアクセストークンを取得
    response = requests.post(url, headers=headers, data=data)
    
    # ステータスコードが200（成功）ならトークンを保存
    if response.status_code == 200:
        print("アクセストークン取得に成功しました")
        token_data = response.json()
        access_token = token_data["access_token"]
        expires_in = token_data["expires_in"]
        
        # 現在の時刻 + 有効期限を保存（UNIXタイムスタンプ）
        expiration_time = time.time() + expires_in
        
        # アクセストークンと有効期限をテキストファイルに保存
        with open("access_token.txt", "w") as token_file:
            json.dump({"access_token": access_token, "expiration_time": expiration_time}, token_file)
        
        print("アクセストークンを保存しました")
        return access_token  # 新しいアクセストークンを返す
    else:
        print(f"トークンの取得に失敗しました。ステータスコード: {response.status_code}")
        print(response.text)

def load_access_token():
    try:
        with open("access_token.txt", "r") as token_file:
            token_data = json.load(token_file)

        # 有効期限をチェック
        if time.time() < token_data["expiration_time"]:
            return token_data["access_token"]
        else:
            print("アクセストークンの有効期限が切れています。再取得してください。")
            return get_access_token()  # トークンの有効期限が切れていたら、新しいトークンを取得して返す

    except FileNotFoundError:
        print("アクセストークンファイルが見つかりません。再取得が必要です。")
        return get_access_token()  # ファイルがない場合も新しいトークンを取得して返す

# # 実行
# get_access_token()
# access_token = load_access_token()
# # アクセストークンを表示
# if access_token:
#     print(f"読み込んだアクセストークン: {access_token}")
# else:
#     print("アクセストークンが無効です。再取得が必要です。")