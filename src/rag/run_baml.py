import os

import lancedb
from baml_client import b
from baml_client.types import Context, Document
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed(text: str) -> list:
    response = OPENAI_CLIENT.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def retrieve_context(query: str, top_k: int = 2):
    tbl = db.open_table("movies")
    query_embedding = embed(query)
    query_builder = tbl.search(query_embedding).limit(top_k).select(["title", "year", "summary", "plot"])
    # BAML model keys cannot begin with underscores
    df = query_builder.to_polars().rename({"_distance": "distance"})
    # Convert to Context objects
    context = [Document(**item) for item in df.to_dicts()]
    return Context(documents=context)


if __name__ == "__main__":
    DB_NAME = "movie_db"
    db = lancedb.connect(DB_NAME)

    questions = [
        "Who does TARS primarily interface with in the movie Interstellar?",
        "What is the special characteristic of Miller's planet in the movie Interstellar?",
    ]
    for question in questions:
        # Query the database
        context = retrieve_context(question)
        answer = b.AnswerQuestion(question, context)
        print(answer)

