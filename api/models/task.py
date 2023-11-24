from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base

# TaskモデルとDoneモデルを定義

class Task(Base):
    __tablename__ = "tasks"                 # テーブル名を定義

    id = Column(Integer, primary_key=True)  # idを主キーに設定
    title = Column(String(1024))

    done = relationship("Done", back_populates="task", cascade="delete")    # Doneモデルとのリレーションを定義


class Done(Base):
    __tablename__ = "dones"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)  # tasksテーブルのidを外部キーに設定

    task = relationship("Task", back_populates="done")