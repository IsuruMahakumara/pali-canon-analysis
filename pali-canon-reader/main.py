import sys
from pathlib import Path

# Add parent directory to path for pali_text_models package
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from natsort import natsorted
from pali_text_models import DictionaryTextModel, ReadingUnitModel, get_engine

# DB
engine = get_engine()

# Static files directory (Svelte build output)
STATIC_DIR = Path(__file__).parent / "svelte-app/static-svelte"



app = FastAPI()


@app.get("/api/reading_unit/{reading_unit_id}")
def get_reading_unit(reading_unit_id: str):
    """Get the text for a reading unit"""
    with Session(engine) as session:
        stmt = select(ReadingUnitModel).where(ReadingUnitModel.reading_unit_id == reading_unit_id).order_by(ReadingUnitModel.index)
        try:
            rows = session.exec(stmt)
            return natsorted(rows.all(), key=lambda x: x.index)
        except Exception as e:
            return {"error": str(e)}


@app.get("/api/dictionary/{entry}")
def get_dictionary(entry: str):
    """Get the definition for a dictionary entry"""
    with Session(engine) as session:
        stmt = select(DictionaryTextModel).where(DictionaryTextModel.entry == entry).o

        try:
            result = session.exec(stmt)
            return result.first()
        except Exception as e:
            return {"error": str(e)}




# Mount static files only if build exists (run `npm run build` in svelte-app first)
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
