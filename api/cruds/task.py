from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result


import api.models.task as task_model
import api.schemas.task as task_schema

# タスク生成用コルーチンの定義
async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate       # task_schemaとTaskCreateを受け取る
) -> task_model.Task:                               # task_model.Taskを返す
    task = task_model.Task(**task_create.dict())    # task_modelに変換する
    db.add(task)                                    # dbに追加する
    await db.commit()
    await db.refresh(task)                          # dbに反映する
    return task


async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    result: Result = await (
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()


async def get_task(db: AsyncSession, task_id: int) -> Optional[task_model.Task]:
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)   # .filterで対象の絞り込み
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    return task[0] if task is not None else None                # 要素が一つであってもtupleで返却されるので値として取り出す


async def update_task(
    db: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task
) -> task_model.Task:
    original.title = task_create.title     # titleを更新する
    db.add(original)        # dbに追加する
    await db.commit()       # dbに反映する
    await db.refresh(original)
    return original


async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()
