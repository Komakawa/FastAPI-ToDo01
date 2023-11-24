# /tasks/{task_id}/doneのリソース実装

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.done as done_schema
import api.cruds.done as done_crud
from api.db import get_db

router = APIRouter()

# チェックボックスにチェックを入れる処理。ON/OFFのみの受付
# チェックする
@router.put("/tasks/{task_id}/done", response_model=done_schema.DoneResponse)
async def mark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):
    done = await done_crud.get_done(db, task_id=task_id)
    if done is not None:
        raise HTTPException(status_code=400, detail="Done already exists")  # チェックがついている場合は400を返す

    return await done_crud.create_done(db, task_id)

# チェックを外す
@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int, db: AsyncSession = Depends(get_db)):    # チェックを外す処理
    done = await done_crud.get_done(db, task_id=task_id)
    if done is None:
        raise HTTPException(status_code=404, detail="Done not found")       # チェックがついていない場合は404を返す

    return await done_crud.delete_done(db, original=done)