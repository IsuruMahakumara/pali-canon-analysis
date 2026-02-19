import sys
from pathlib import Path

# Add parent directory to path for pali_text_models package
sys.path.insert(0, str(Path(__file__).parent.parent))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select, func, col
from natsort import natsorted
from init_db import init_db
from pali_text_models import SuttaTextModel, get_engine

# DB
engine = get_engine()

# Static files directory (Svelte build output)
STATIC_DIR = Path(__file__).parent / "static-svelte"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/nikayas")
def list_nikayas():
    """List all nikayas with their sutta counts"""
    with Session(engine) as session:
        stmt = (
            select(
                SuttaTextModel.nikaya,
                func.count(func.distinct(SuttaTextModel.sutta_id)).label("count")
            )
            .where(SuttaTextModel.sutta_id != "")
            .group_by(SuttaTextModel.nikaya)
            .order_by(SuttaTextModel.nikaya)
        )
        result = session.exec(stmt)
        return [{"id": nikaya, "count": count} for nikaya, count in result]


@app.get("/api/suttas/{nikaya}")
def list_suttas_by_nikaya(nikaya: str):
    """List all sutta_ids for a specific nikaya"""
    with Session(engine) as session:
        stmt = (
            select(SuttaTextModel.sutta_id)
            .where(SuttaTextModel.nikaya == nikaya, SuttaTextModel.sutta_id != "")
            .distinct()
        )
        result = session.exec(stmt)
        return natsorted(result.all())


@app.get("/api/sutta/{sutta_id}")
def get_sutta(sutta_id: str):
    """Get all verses for a sutta (pali + hela)"""
    with Session(engine) as session:
        stmt = select(SuttaTextModel).where(SuttaTextModel.sutta_id == sutta_id)
        result = session.exec(stmt)
        return natsorted(result.all(), key=lambda x: x.index)


# Mount static files only if build exists (run `npm run build` in svelte-app first)
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
