###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> Gemini15Flash {\n  provider google-ai\n  options {\n    model \"gemini-1.5-flash\"\n    api_key env.GOOGLE_API_KEY\n    generationConfig {\n      temperature 0.3\n    }\n  }\n}\n\n\nclient<llm> Gemini2FlashLite {\n  provider google-ai\n  options {\n    model \"gemini-2.0-flash-lite-preview-02-05\"\n    api_key env.GOOGLE_API_KEY\n    generationConfig {\n      temperature 0.3\n    }\n  }\n}\n\nclient<llm> CustomGPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> GeneratorGPT4oMini {\n  provider openai\n  retry_policy Exponential\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n    temperature 0.3\n  }\n}\n\nclient<llm> CustomSonnet {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20241022\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n\nclient<llm> CustomHaiku {\n  provider anthropic\n  retry_policy Constant\n  options {\n    model \"claude-3-haiku-20240307\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/round-robin\nclient<llm> CustomFast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    strategy [GeneratorGPT4oMini, CustomHaiku]\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/fallback\nclient<llm> OpenaiFallback {\n  provider fallback\n  options {\n    // This will try the clients in order until one succeeds\n    strategy [GeneratorGPT4oMini, GeneratorGPT4oMini]\n  }\n}\n\n// https://docs.boundaryml.com/docs/snippets/clients/retry\nretry_policy Constant {\n  max_retries 3\n  // Strategy is optional\n  strategy {\n    type constant_delay\n    delay_ms 200\n  }\n}\n\nretry_policy Exponential {\n  max_retries 2\n  // Strategy is optional\n  strategy {\n    type exponential_backoff\n    delay_ms 300\n    mutliplier 1.5\n    max_delay_ms 10000\n  }\n}",
    "generators.baml": "// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\", \"rest/openapi\"\n    output_type \"python/pydantic\"\n\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../\"\n\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.75.0\"\n\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    default_client_mode sync\n}\n",
    "rag.baml": "// --- Data models ---\nclass Query {\n  query string\n}\n\nclass Answer {\n  question string\n  answer string\n}\n\n// --- Functions ---\n\nfunction Text2Cypher(schema: string, question: string) -> Query | null {\n  client Gemini15Flash\n  prompt #\"\n    You are an expert in translating natural language questions into Cypher statements.\n    You will be provided with a question and a graph schema.\n    Use only the provided relationship types and properties in the schema to generate a Cypher\n    statement.\n    The Cypher statement could retrieve nodes, relationships, or both.\n    Do not include any explanations or apologies in your responses.\n    Do not respond to any questions that might ask anything else than for you to construct a\n    Cypher statement.\n    Generate the answer in 1-3 sentences.\n\n    {{ _.role(\"user\") }}\n    Task: Generate a Cypher statement to query a graph database.\n\n    {{ schema}}\n\n    The question is:\n    {{ question }}\n\n    Instructions:\n    1. Use only the provided node and relationship types and properties in the schema.\n    2. When returning results, return property values rather than the entire node or relationship.\n    3. When using the WHERE clause to compare string properties, use the LOWER() function.\n\n    {{ ctx.output_format }}\n  \"#\n}\n\nfunction AnswerQuestion(context: Answer) -> Answer {\n  client Gemini15Flash\n  prompt #\"\n    Answer the question in full sentences using the provided context.\n    Do not make up an answer. If you don't know the answer, say that you do not have the required context.\n\n    {{ _.role(\"user\") }}\n    QUESTION: {{ context.question }}\n    RELEVANT CONTEXT: {{ context.answer }}\n\n    {{ ctx.output_format }}\n\n    RESPONSE:\n  \"#\n}\n\n// --- Test cases ---\n\ntest cypher_1 {\n  functions [Text2Cypher]\n  args {\n    schema #\"\n    ALWAYS RESPECT THE EDGE DIRECTIONS:\n    ---\n    (:Actor) -[:ACTED_IN]-> (:Movie)\n    (:Character) -[:PLAYED_ROLE_IN]-> (:Movie)\n    (:Director) -[:DIRECTED]-> (:Movie)\n    (:Actor) -[:PLAYED]-> (:Character)\n    (:Character) -[:RELATED_TO]-> (:Character)\n    (:Writer) -[:WROTE]-> (:Movie)\n    ---\n\n    Node properties:\n    - Movie\n        - title: string\n        - year: int64\n        - summary: string\n    - Director\n        - name: string\n        - age: int64\n    - Character\n        - name: string\n        - description: string\n    - Actor\n        - name: string\n        - age: int64\n    - Writer\n        - name: string\n        - age: int64\n\n    Edge properties:\n    - RELATED_TO\n        - relationship: string\n    \"#\n    question \"Name the actors who acted in the movies directed by Christopher Nolan?\"\n  }\n}\n\ntest cypher_2 {\n  functions [Text2Cypher]\n  args {\n    schema #\"\n    ALWAYS RESPECT THE EDGE DIRECTIONS:\n    ---\n    (:Actor) -[:ACTED_IN]-> (:Movie)\n    (:Character) -[:PLAYED_ROLE_IN]-> (:Movie)\n    (:Director) -[:DIRECTED]-> (:Movie)\n    (:Actor) -[:PLAYED]-> (:Character)\n    (:Character) -[:RELATED_TO]-> (:Character)\n    (:Writer) -[:WROTE]-> (:Movie)\n    ---\n\n    Node properties:\n    - Movie\n        - title: string\n        - year: int64\n        - summary: string\n    - Director\n        - name: string\n        - age: int64\n    - Character\n        - name: string\n        - description: string\n    - Actor\n        - name: string\n        - age: int64\n    - Writer\n        - name: string\n        - age: int64\n\n    Edge properties:\n    - RELATED_TO\n        - relationship: string\n    \"#\n    question \"Which actor played the character Murphy Cooper in the movie Interstellar?\"\n  }\n}\n\ntest answer_question_1 {\n  functions [AnswerQuestion]\n  args {\n    context {\n      question \"Name the actors who acted in the movies directed by Christopher Nolan?\",\n      answer \"['Michael Caine', 'Anne Hathaway', 'Matthew McConaughey', 'Casey Affleck', 'Jessica Chastain']\"\n    }\n  }\n}\n\ntest answer_question_2 {\n  functions [AnswerQuestion]\n  args {\n    context {\n      question \"Which actor played the character Murphy Cooper in the movie Interstellar?\",\n      answer \"['Jessica Chastain']\"\n    }\n  }\n}\n\n\ntest missing_context {\n  functions [AnswerQuestion]\n  args {\n    context {\n      question \"Which actor played the character Murphy Cooper in the movie Interstellar?\",\n      answer \"\"\n    }\n  }\n}\n",
}

def get_baml_files():
    return file_map