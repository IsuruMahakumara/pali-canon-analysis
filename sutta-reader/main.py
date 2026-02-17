from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Field, SQLModel, Session, create_engine, select, text
from natsort import natsorted
from init_db import init_db

# Model
class Sutta(SQLModel, table=True):
    index: str = Field(primary_key=True)
    nikaya: str
    vagga: str
    sutta_id: str
    text: str | None
    hela_text: str | None

# DB
engine = create_engine("duckdb:///pali_canon.db", echo=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/api/nikayas")
def list_nikayas():
    """List all nikayas with their sutta counts"""
    with Session(engine) as s:
        result = s.exec(text(
            "SELECT nikaya, COUNT(DISTINCT sutta_id) as count FROM sutta WHERE sutta_id != '' GROUP BY nikaya ORDER BY nikaya"
        ))
        return [{"id": r[0], "count": r[1]} for r in result]

@app.get("/api/suttas/{nikaya}")
def list_suttas_by_nikaya(nikaya: str):
    """List all sutta_ids for a specific nikaya"""
    with Session(engine) as s:
        result = s.exec(text(
            f"SELECT DISTINCT sutta_id FROM sutta WHERE nikaya = :nikaya AND sutta_id != ''"
        ).bindparams(nikaya=nikaya))
        return natsorted([r[0] for r in result])

@app.get("/api/sutta/{sutta_id}")
def get_sutta(sutta_id: str):
    """Get all verses for a sutta (pali + hela)"""
    with Session(engine) as s:
        result = s.exec(
            select(Sutta).where(Sutta.sutta_id == sutta_id)
        )
        return natsorted(result.all(), key=lambda x: x.index)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
