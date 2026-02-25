"""Initialize PostgreSQL database from CSV"""
import sys
from pathlib import Path

# Add parent directory to path for pali_text_models package
sys.path.insert(0, str(Path(__file__).parent.parent))

import csv
from sqlmodel import Session, select
from pali_text_models import SuttaTextModel, get_engine, create_tables

CSV_PATH = Path(__file__).parent.parent / "pali_canon_hela.csv"


def init_db():
    """Initialize sutta_texts table from CSV (only if empty)"""
    engine = get_engine()
    
    # Create tables if they don't exist
    create_tables(engine)
    
    with Session(engine) as session:
        # Check if data already exists
        existing = session.exec(select(SuttaTextModel).limit(1)).first()
        if existing:
            print("Database already initialized, skipping CSV load")
            return
        
        # Load from CSV
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                sutta = SuttaTextModel(
                    index=row['index'],
                    nikaya=row['nikaya'],
                    vagga=row['vagga'],
                    sutta_id=row['sutta_id'],
                    text=row.get('text'),
                    hela_text=row.get('hela_text')
                )
                session.add(sutta)
                count += 1
            
            session.commit()
            print(f"Loaded {count} verses")


if __name__ == "__main__":
    init_db()
