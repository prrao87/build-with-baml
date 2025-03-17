import os
import shutil

import lancedb
import polars as pl
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed(text: str) -> list:
    response = OPENAI_CLIENT.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


if __name__ == "__main__":
    data = pl.read_csv("../../data/movies/nodes/movie.csv", has_header=False, separator="|", new_columns=["title", "year", "summary", "plot"])
    # Generate embeddings for the plot column
    data = data.with_columns(
        pl.col("plot").map_elements(embed, return_dtype=pl.List(pl.Float64)).alias("vector")
    )

    DB_NAME = "movie_db"
    shutil.rmtree(DB_NAME, ignore_errors=True)
    db = lancedb.connect(DB_NAME)

    tbl = db.create_table("movies", data, mode="overwrite")
    print("Finished ingesting data")


