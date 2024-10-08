import os
import requests # type: ignore
from dotenv import load_dotenv

def post_collectstart_to_api(token):
    device_id = os.getenv('DEVICE_ID')
    url = f"https://console.aitrios.sony-semicon.com/api/v1/devices/{device_id}/inferenceresults/collectstart"
    
    # 認証のためのヘッダー
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"APIリクエストを送信中: {url}")
    print(f"使用するトークン: {token}")
    
    try:
        # POSTリクエストを送信
        response = requests.post(url, headers=headers, timeout=10)  # タイムアウトを10秒に設定

        print(f"レスポンスのステータスコード: {response.status_code}")

        # レスポンスの確認
        response.raise_for_status()  # ステータスコードが200番台以外なら例外を発生させる

        # JSONレスポンスを返す
        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid JSON response"}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def post_collectstop_to_api(token):
    device_id = os.getenv('DEVICE_ID')
    url = f"https://console.aitrios.sony-semicon.com/api/v1/devices/{device_id}/inferenceresults/collectstop"
    
    # 認証のためのヘッダー
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # POSTリクエストを送信
        response = requests.post(url, headers=headers, timeout=10)  # タイムアウトを10秒に設定

        # レスポンスの確認
        response.raise_for_status()  # ステータスコードが200番台以外なら例外を発生させる

        # JSONレスポンスを返す
        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid JSON response"}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
