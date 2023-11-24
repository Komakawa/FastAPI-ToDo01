from fastapi import FastAPI

from api.routers import task, done

app = FastAPI()     # FastAPIのインスタンス作成
# SwaggerUIの設定
# routerをincludeすることで、各routerのpathがSwaggerUIに表示される
app.include_router(task.router)
app.include_router(done.router)

@app.get("/hello")  # サンプルデコレータの定義
# サンプルのレスポンス
# http://localhost:8000/helloでアクセスできる
async def hello():
    return {"message": "hello world!"}