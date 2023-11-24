from typing import Optional

from pydantic import BaseModel, Field

# デフォルトのタスク内容を定義
# BaseModelを継承しているので、Pydanticの機能が使える
class TaskBase(BaseModel):
    title: Optional[str] = Field(None, example="Buy milk")

# titleのみを定義するために、両方のベースクラスであるTaskBaseを継承
class TaskCreate(TaskBase):
    pass

# Taskとしてidとdoneを付与したものを定義
class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True

# Createのレスポンスとしてidだけを付与したものを定義
class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True
