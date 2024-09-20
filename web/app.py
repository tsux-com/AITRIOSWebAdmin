from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from api_services.service import post_collectstart_to_api, post_collectstop_to_api
from access_token import load_access_token


# FastAPIのインスタンスを作成
app = FastAPI()

# Jinja2テンプレートの設定
templates = Jinja2Templates(directory="templates")

# ルートエンドポイントにアクセスした際に HTML を返す
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 毎回トークンをロードして使用
    token = load_access_token()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "message": "Click the button to start the API call",
        "token": token
    })

# ボタンがクリックされた際に呼び出されるエンドポイント
@app.post("/start-api")
async def start_api():
     # 毎回トークンをロードして使用
    token = load_access_token()
    
    # APIを呼び出す
    api_response = post_collectstart_to_api(token)
    
    # APIレスポンスを返す
    return api_response

# ボタンがクリックされた際に呼び出されるエンドポイント
@app.post("/stop-api")
async def start_api():
    # 毎回トークンをロードして使用
    token = load_access_token()
    
    # APIを呼び出す
    api_response = post_collectstop_to_api(token)
    
    # APIレスポンスを返す
    return api_response