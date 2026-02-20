"""Strawberry GraphQL schema for flat/normalized graph data"""
import strawberry
from typing import Any
import age_query


@strawberry.type
class Node:
    """Graph node in flat format"""
    id: str
    label: str
    properties: strawberry.scalars.JSON


@strawberry.type
class Edge:
    """Graph edge in flat format"""
    id: str
    source: str
    target: str
    label: str
    properties: strawberry.scalars.JSON


@strawberry.type
class FlatGraph:
    """Normalized graph: separate lists of nodes and edges"""
    nodes: list[Node]
    edges: list[Edge]


def _extract_node(data: dict) -> Node:
    """Extract Node from Age result."""
    props = data.get("properties", {})
    node_id = props.pop("id", str(data.get("id", "")))
    label = data.get("label", "")
    return Node(id=node_id, label=label, properties=props)


def _extract_edge(data: dict) -> Edge:
    """Extract Edge from Age result."""
    props = data.get("properties", {})
    edge_id = str(data.get("id", ""))
    source = str(data.get("start_id", ""))
    target = str(data.get("end_id", ""))
    label = data.get("label", "")
    return Edge(id=edge_id, source=source, target=target, label=label, properties=props)


@strawberry.type
class Query:
    @strawberry.field
    def nodes(self, label: str | None = None, limit: int = 100) -> list[Node]:
        """Get nodes, optionally filtered by label."""
        results = age_query.get_nodes(label=label, limit=limit)
        return [_extract_node(r) for r in results]

    @strawberry.field
    def edges(self, rel_type: str | None = None, limit: int = 100) -> list[Edge]:
        """Get edges, optionally filtered by relationship type."""
        results = age_query.get_edges(rel_type=rel_type, limit=limit)
        return [_extract_edge(r) for r in results]

    @strawberry.field
    def node(self, id: str) -> Node | None:
        """Get single node by id."""
        result = age_query.get_node_by_id(id)
        return _extract_node(result) if result else None

    @strawberry.field
    def subgraph(self, node_id: str, direction: str = "both", limit: int = 50) -> FlatGraph:
        """Get subgraph around a node (neighbors + edges)."""
        results = age_query.get_neighbors(node_id, direction=direction, limit=limit)
        
        nodes_map: dict[str, Node] = {}
        edges_list: list[Edge] = []
        
        for row in results:
            # row is {n: node, r: edge, m: neighbor}
            if row.get("n"):
                node = _extract_node(row["n"])
                nodes_map[node.id] = node
            if row.get("m"):
                node = _extract_node(row["m"])
                nodes_map[node.id] = node
            if row.get("r"):
                edges_list.append(_extract_edge(row["r"]))
        
        return FlatGraph(nodes=list(nodes_map.values()), edges=edges_list)

    @strawberry.field
    def cypher(self, query: str, columns: list[str] | None = None) -> strawberry.scalars.JSON:
        """Execute raw Cypher query. Provide column names matching your RETURN aliases."""
        return age_query.run_cypher(query, columns=columns)


schema = strawberry.Schema(query=Query)

