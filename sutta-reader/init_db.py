"""Initialize DuckDB from CSV"""
import duckdb

CREATE_SQL = """
CREATE TABLE sutta AS 
SELECT * FROM read_csv('../pali_canon_hela.csv', 
    columns={
        'index': 'VARCHAR',
        'nikaya': 'VARCHAR', 
        'vagga': 'VARCHAR',
        'sutta_id': 'VARCHAR',
        'text': 'VARCHAR',
        'hela_text': 'VARCHAR'
    },
    header=true
)
"""

def init_db():
    """Recreate sutta table from CSV on every startup"""
    with duckdb.connect('pali_canon.db') as con:
        con.sql("DROP TABLE IF EXISTS sutta")
        con.sql("CREATE TABLE sutta AS SELECT * FROM '../pali_canon_hela.csv'")
        count = con.sql('SELECT COUNT(*) FROM sutta').fetchone()[0]
        print(f"Loaded {count} verses")


if __name__ == "__main__":
    init_db()

