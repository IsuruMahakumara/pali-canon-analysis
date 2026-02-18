"""Initialize PostgreSQL database from CSV"""
import sys
from pathlib import Path

# Add parent directory to path for pali_text_models package
sys.path.insert(0, str(Path(__file__).parent.parent))

import csv
from sqlmodel import Session, text
from pali_text_models import Sutta, get_engine, create_tables

CSV_PATH = Path(__file__).parent.parent / "pali_canon_hela.csv"


def init_db():
    """Recreate sutta table from CSV on every startup"""
    engine = get_engine()
    
    # Create tables if they don't exist
    create_tables(engine)
    
    with Session(engine) as session:
        # Clear existing data
        session.exec(text("TRUNCATE TABLE sutta"))
        session.commit()
        
        # Load from CSV
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                sutta = Sutta(
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
