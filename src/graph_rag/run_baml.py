import kuzu
from baml_client import b
from baml_client.types import Answer


class GetSchema:
    """Get schema information from Kuzu database"""

    def __init__(self, conn: kuzu.Connection):
        self.conn = conn

    def get_schema_dict(self) -> dict[str, list[dict]]:
        # Get schema for LLM
        nodes = self.conn._get_node_table_names()
        relationships = self.conn._get_rel_table_names()

        schema = {"nodes": [], "edges": []}

        for node in nodes:
            node_schema = {"label": node, "properties": []}
            node_properties = self.conn.execute(f"CALL TABLE_INFO('{node}') RETURN *;")
            while node_properties.has_next():
                row = node_properties.get_next()
                node_schema["properties"].append({"name": row[1], "type": row[2]})
            schema["nodes"].append(node_schema)

        for rel in relationships:
            edge = {"label": rel["name"], "src": rel["src"], "dst": rel["dst"], "properties": []}
            rel_properties = self.conn.execute(f"""CALL TABLE_INFO('{rel["name"]}') RETURN *;""")
            while rel_properties.has_next():
                row = rel_properties.get_next()
                edge["properties"].append({"name": row[1], "type": row[2]})
            schema["edges"].append(edge)

        return schema

    def get_schema_baml(self) -> str:
        schema = self.get_schema_dict()
        lines = []

        # ALWAYS RESPECT THE RELATIONSHIP DIRECTIONS section
        lines.append("ALWAYS RESPECT THE EDGE DIRECTIONS:\n---")
        for edge in schema.get("edges", []):
            lines.append(f"(:{edge['src']}) -[:{edge['label']}]-> (:{edge['dst']})")
        lines.append("---")

        # NODES section
        lines.append("\nNode properties:")
        for node in schema.get("nodes", []):
            lines.append(f"  - {node['label']}")
            for prop in node.get("properties", []):
                ptype = prop["type"].lower()
                lines.append(f"    - {prop['name']}: {ptype}")

        # EDGES section (only include edges with properties)
        lines.append("\nEdge properties:")
        for edge in schema.get("edges", []):
            if edge.get("properties"):
                lines.append(f"- {edge['label']}")
                for prop in edge.get("properties", []):
                    ptype = prop["type"].lower()
                    lines.append(f"    - {prop['name']}: {ptype}")
        return "\n".join(lines)


def run_query(conn: kuzu.Connection, question: str, cypher: str) -> Answer:
    """Use the generated Cypher statement to query the graph database."""
    response = conn.execute(cypher)
    result = []
    while response.has_next():
        item = response.get_next()
        if item not in result:
            result.extend(item)

    # Handle both hashable and non-hashable types
    if all(isinstance(x, (str, int, float, bool, tuple)) for x in result):
        final_result = {"question": question, "answer": str(list(set(result)))}
    else:
        # For non-hashable types, we can't use set() directly
        # Instead, we'll use a list comprehension to remove duplicates
        final_result = {
            "question": question,
            "answer": str([x for i, x in enumerate(result) if x not in result[:i]]),
        }
    # parse the result into an Answer object
    return Answer(**final_result)


if __name__ == "__main__":
    db = kuzu.Database("test_kuzudb")
    conn = kuzu.Connection(db)
    schema_generator = GetSchema(conn)
    baml_schema = schema_generator.get_schema_baml()
    questions = [
        # "Can you tell me about Joseph Cooper and his daughter Murphy Cooper?",
        "Which actor played the character Murphy Cooper in the movie Interstellar?",
        # "Name the actors who acted in the movies directed by Christopher Nolan?",
    ]
    for question in questions:
        output = b.Text2Cypher(baml_schema, question)

        # Query the database
        if output:
            cypher = output.query
            print(cypher)
            context = run_query(conn, question, cypher)
            print(context)
            answer = b.AnswerQuestion(context)
            print(answer)
