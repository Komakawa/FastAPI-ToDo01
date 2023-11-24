from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Dockerのコンテナ名を指定しMySQLと接続するセッション
ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True) # echo=TrueでSQLのログを出力する
async_session = sessionmaker(                               # sessionmakerでセッションを作成
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession   # autocommit=False, autoflush=Falseでトランザクションを明示的に指定する
)

Base = declarative_base()

# DBへのアクセスを行う関数
async def get_db():
    async with async_session() as session:  # sessionを取得
        yield session