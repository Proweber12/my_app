import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, engine, create_engine, Field, Session, select
from pydantic import BaseSettings
import sqlalchemy

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Settings(BaseSettings):
    bd_url: str = "postgresql://mihail:mihail@db:5432/mihail"
    bd_echo: bool = True


settings = Settings()


def get_engine() -> engine:
    sql_engine = create_engine(settings.bd_url, echo=settings.bd_echo)
    return sql_engine


sql_engine = get_engine()
session = Session(sql_engine)


class Data(SQLModel, table=True):
    __tablename__ = "datas"
    id: int = Field(primary_key=True)
    name: str
    desc: str
    

@app.on_event("startup")
async def init():
    SQLModel.metadata.create_all(sql_engine)


@app.get("/")
async def hello_world():
    global session
    query = select(Data)
    return session.exec(query).all()