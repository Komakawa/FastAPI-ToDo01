# /tasksのリソース実装

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task as task_crud
from api.db import get_db

import api.schemas.task as task_schema

router = APIRouter()

# APIのリクエストとレスポンスを実装

# createした回数だけタスクが生成される
@router.get("/tasks", response_model=List[task_schema.Task])    # GET /tasksのリクエストを受け付ける
async def list_tasks(db: AsyncSession = Depends(get_db)):       # リクエストを受け付けたら、dbを取得
    return await task_crud.get_tasks_with_done(db)              # dbを引数に、get_tasks_with_doneを実行


# POSTのパスオペレーション関数を実装
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)       #schemaを指定し、POST /tasksのリクエストを受け付ける
async def create_task(
    task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)   # リクエストボディを受け取る
):
    return await task_crud.create_task(db, task_body)                       # dbとリクエストボディを引数にcreate_taskを実行suru


@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)  # リクエストボディを受け取る
    ):
    task = await task_crud.get_task(db, task_id=task_id)                    # task_idを引数にget_taskを実行
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")       # タスクが見つからない場合は404を返す

    return await task_crud.update_task(db, task_body, original=task)


@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)

