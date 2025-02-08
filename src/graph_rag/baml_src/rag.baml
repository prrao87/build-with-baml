// --- Data models ---
class Query {
  query string
}

class Answer {
  question string
  answer string
}

// --- Functions ---

function Text2Cypher(schema: string, question: string) -> Query | null {
  client Gemini15Flash
  prompt #"
    You are an expert in translating natural language questions into Cypher statements.
    You will be provided with a question and a graph schema.
    Use only the provided relationship types and properties in the schema to generate a Cypher
    statement.
    The Cypher statement could retrieve nodes, relationships, or both.
    Do not include any explanations or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a
    Cypher statement.
    Generate the answer in 1-3 sentences.

    {{ _.role("user") }}
    Task: Generate a Cypher statement to query a graph database.

    {{ schema}}

    The question is:
    {{ question }}

    Instructions:
    1. Use only the provided node and relationship types and properties in the schema.
    2. When returning results, return property values rather than the entire node or relationship.
    3. When using the WHERE clause to compare string properties, use the LOWER() function.

    {{ ctx.output_format }}
  "#
}

function AnswerQuestion(context: Answer) -> Answer {
  client Gemini15Flash
  prompt #"
    Answer the question in full sentences using the provided context.
    Do not make up an answer. If you don't know the answer, say that you do not have the required context.

    {{ _.role("user") }}
    QUESTION: {{ context.question }}
    RELEVANT CONTEXT: {{ context.answer }}

    {{ ctx.output_format }}

    RESPONSE:
  "#
}

// --- Test cases ---

test cypher_1 {
  functions [Text2Cypher]
  args {
    schema #"
    ALWAYS RESPECT THE EDGE DIRECTIONS:
    ---
    (:Actor) -[:ACTED_IN]-> (:Movie)
    (:Character) -[:PLAYED_ROLE_IN]-> (:Movie)
    (:Director) -[:DIRECTED]-> (:Movie)
    (:Actor) -[:PLAYED]-> (:Character)
    (:Character) -[:RELATED_TO]-> (:Character)
    (:Writer) -[:WROTE]-> (:Movie)
    ---

    Node properties:
    - Movie
        - title: string
        - year: int64
        - summary: string
    - Director
        - name: string
        - age: int64
    - Character
        - name: string
        - description: string
    - Actor
        - name: string
        - age: int64
    - Writer
        - name: string
        - age: int64

    Edge properties:
    - RELATED_TO
        - relationship: string
    "#
    question "Name the actors who acted in the movies directed by Christopher Nolan?"
  }
}

test cypher_2 {
  functions [Text2Cypher]
  args {
    schema #"
    ALWAYS RESPECT THE EDGE DIRECTIONS:
    ---
    (:Actor) -[:ACTED_IN]-> (:Movie)
    (:Character) -[:PLAYED_ROLE_IN]-> (:Movie)
    (:Director) -[:DIRECTED]-> (:Movie)
    (:Actor) -[:PLAYED]-> (:Character)
    (:Character) -[:RELATED_TO]-> (:Character)
    (:Writer) -[:WROTE]-> (:Movie)
    ---

    Node properties:
    - Movie
        - title: string
        - year: int64
        - summary: string
    - Director
        - name: string
        - age: int64
    - Character
        - name: string
        - description: string
    - Actor
        - name: string
        - age: int64
    - Writer
        - name: string
        - age: int64

    Edge properties:
    - RELATED_TO
        - relationship: string
    "#
    question "Which actor played the character Murphy Cooper in the movie Interstellar?"
  }
}

test answer_question_1 {
  functions [AnswerQuestion]
  args {
    context {
      question "Name the actors who acted in the movies directed by Christopher Nolan?",
      answer "['Michael Caine', 'Anne Hathaway', 'Matthew McConaughey', 'Casey Affleck', 'Jessica Chastain']"
    }
  }
}

test answer_question_2 {
  functions [AnswerQuestion]
  args {
    context {
      question "Which actor played the character Murphy Cooper in the movie Interstellar?",
      answer "['Jessica Chastain']"
    }
  }
}


test missing_context {
  functions [AnswerQuestion]
  args {
    context {
      question "Which actor played the character Murphy Cooper in the movie Interstellar?",
      answer ""
    }
  }
}
