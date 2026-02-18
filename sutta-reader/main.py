import sys
from pathlib import Path

# Add parent directory to path for pali_text_models package
sys.path.insert(0, str(Path(__file__).parent.parent))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select, text
from natsort import natsorted
from init_db import init_db
from pali_text_models import Sutta, get_engine

# DB
engine = get_engine()

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
            "SELECT DISTINCT sutta_id FROM sutta WHERE nikaya = :nikaya AND sutta_id != ''"
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
