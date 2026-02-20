"""Simple Apache Age query wrapper for pali_canon_graph"""
import json
import psycopg
from typing import Any

# Connection string for pali_canon_db
CONN_STR = "host=localhost dbname=pali_canon_db user=pali_canon password=anicca"
GRAPH_NAME = "pali_canon_graph"


def _parse_agtype(val: Any) -> Any:
    """Parse agtype value to Python dict/list."""
    if val is None:
        return None
    if isinstance(val, str):
        # Age returns JSON strings with ::vertex, ::edge suffixes - strip them
        clean = val.split("::")[0] if "::" in val else val
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            return val
    return val


def run_cypher(query: str, columns: list[str] = None) -> list[Any]:
    """Execute a Cypher query on pali_canon_graph.
    
    columns: list of column names for multi-value RETURN clauses.
             If None, assumes single column 'result'.
    """
    columns = columns or ["result"]
    col_def = ", ".join(f"{c} agtype" for c in columns)
    
    with psycopg.connect(CONN_STR) as conn:
        with conn.cursor() as cur:
            cur.execute("LOAD 'age';")
            cur.execute("SET search_path = ag_catalog, '$user', public;")
            
            cypher_sql = f"SELECT * FROM cypher('{GRAPH_NAME}', $$ {query} $$) AS ({col_def});"
            cur.execute(cypher_sql)
            
            rows = cur.fetchall()
            if len(columns) == 1:
                return [_parse_agtype(row[0]) for row in rows]
            else:
                # Return list of dicts with column names as keys
                return [
                    {col: _parse_agtype(row[i]) for i, col in enumerate(columns)}
                    for row in rows
                ]


def get_nodes(label: str | None = None, limit: int = 100) -> list[dict]:
    """Get nodes, optionally filtered by label."""
    if label:
        q = f"MATCH (n:{label}) RETURN n LIMIT {limit}"
    else:
        q = f"MATCH (n) RETURN n LIMIT {limit}"
    return run_cypher(q)


def get_edges(rel_type: str | None = None, limit: int = 100) -> list[dict]:
    """Get edges, optionally filtered by relationship type."""
    if rel_type:
        q = f"MATCH ()-[r:{rel_type}]->() RETURN r LIMIT {limit}"
    else:
        q = f"MATCH ()-[r]->() RETURN r LIMIT {limit}"
    return run_cypher(q)


def get_node_by_id(node_id: str) -> dict | None:
    """Get a single node by its id property."""
    q = f"MATCH (n {{id: '{node_id}'}}) RETURN n LIMIT 1"
    result = run_cypher(q)
    return result[0] if result else None


def get_neighbors(node_id: str, direction: str = "both", limit: int = 50) -> list[dict]:
    """Get neighboring nodes and edges for a node. Returns list of {n, r, m} dicts."""
    if direction == "out":
        q = f"MATCH (n {{id: '{node_id}'}})-[r]->(m) RETURN n, r, m LIMIT {limit}"
    elif direction == "in":
        q = f"MATCH (n {{id: '{node_id}'}})<-[r]-(m) RETURN n, r, m LIMIT {limit}"
    else:
        q = f"MATCH (n {{id: '{node_id}'}})-[r]-(m) RETURN n, r, m LIMIT {limit}"
    return run_cypher(q, columns=["n", "r", "m"])
