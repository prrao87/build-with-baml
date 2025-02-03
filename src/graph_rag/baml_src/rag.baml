class Query {
  query string
}

// --- Functions ---

function Text2Cypher(schema: string, question: string) -> Query | null {
  client CustomGPT4oMini
  prompt #"
    {{ _.role("system") }}
    You are an expert in translating natural language questions into Cypher statements.
    You will be provided with a question and a graph schema.
    Use only the provided relationship types and properties in the schema to generate a Cypher
    statement.
    The Cypher statement could retrieve nodes, relationships, or both.
    Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a
    Cypher statement.

    {{ _.role("user") }}
    Schema:
    {{ schema }}

    {{ ctx.output_format }}

    Question:
    {{ question }}

    Instructions:
    - When querying a property, always lowercase the property using the LOWER() function.
    - For contains queries, use the CONTAINS() function. e.g. `CONTAINS(property, user_query_term)`
  "#
}

// --- Test cases ---

test rhea_knows_jon {
  functions [Text2Cypher]
  args {
    schema #"
    ALWAYS RESPECT THE EDGE DIRECTIONS:
    ---
    - Person -> KNOWS -> Person
    - Person -> WORKS_AT -> Company
    ---

    NODES:
    - Person
        - name: string
        - age: int64
    - Company
        - name: string

    EDGES:
    - KNOWS
        - since: INT64
    "#
    question "Since which year does Rhea know Jon?"
  }
}

test rhea_works_at_apple {
  functions [Text2Cypher]
  args {
    schema #"
    ALWAYS RESPECT THE EDGE DIRECTIONS:
    ---
    - Person -> KNOWS -> Person
    - Person -> WORKS_AT -> Company
    ---

    NODES:
    - Person
        - name: string
        - age: int64
    - Company
        - name: string

    EDGES:
    - KNOWS
        - since: INT64
    "#
    question "What company does Rhea work at?"
  }
}
