from fastapi import FastAPI

from api.routers import task, done

app = FastAPI()     # appはFastAPIのインスタンス
app.include_router(task.router)
app.include_router(done.router)

@app.get("/hello")  # @で始まる部分をデコレータと呼ぶ
async def hello():
    return {"message": "hello world!"}