"""
Create a graph in Kùzu
"""
import shutil

import kuzu
import polars as pl

shutil.rmtree("test_kuzudb", ignore_errors=True)
db = kuzu.Database("test_kuzudb")
conn = kuzu.Connection(db)


# Define schema
conn.execute("""
    CREATE NODE TABLE IF NOT EXISTS Actor(name STRING PRIMARY KEY, age INT64);
    CREATE NODE TABLE IF NOT EXISTS Movie(title STRING PRIMARY KEY, year INT64, summary STRING, plot STRING);
    CREATE NODE TABLE IF NOT EXISTS Director(name STRING PRIMARY KEY, age INT64);
    CREATE NODE TABLE IF NOT EXISTS Character(name STRING PRIMARY KEY, description STRING);
    CREATE NODE TABLE IF NOT EXISTS Writer(name STRING PRIMARY KEY, age INT64);
    CREATE REL TABLE IF NOT EXISTS ACTED_IN(FROM Actor TO Movie);
    CREATE REL TABLE IF NOT EXISTS PLAYED(FROM Actor TO Character);
    CREATE REL TABLE IF NOT EXISTS DIRECTED(FROM Director TO Movie);
    CREATE REL TABLE IF NOT EXISTS PLAYED_ROLE_IN(FROM Character TO Movie);
    CREATE REL TABLE IF NOT EXISTS RELATED_TO(FROM Character TO Character, relationship STRING);
    CREATE REL TABLE IF NOT EXISTS WROTE(FROM Writer TO Movie);
""")

# Ingest data
base_path = "../../data"
files = {
    "Actor": "actor.csv",
    "Director": "director.csv",
    "Character": "character.csv",
    "Writer": "writer.csv",
    "ACTED_IN": "acted_in.csv",
    "DIRECTED": "directed.csv",
    "PLAYED": "played.csv",
    "PLAYED_ROLE_IN": "played_role_in.csv",
    "RELATED_TO": "related_to.csv",
    "WROTE": "wrote.csv",
}

# Read in movie data with a `|` separator instead as this file is formatted differently
conn.execute(f"COPY Movie FROM '{base_path}/movie.csv' (DELIM='|');")

# Read in the rest of the data
for table, file in files.items():
    conn.execute(f"COPY {table} FROM '{base_path}/{file}';")


print("Finished ingesting data")

# Use an OpenAI embedding model to store a vector embedding of the "summary" property in the movie node
df = pl.read_csv(
    f"{base_path}/movie.csv",
    has_header=False,
    separator="|",
).rename({
    "column_1": "title",
    "column_2": "year",
    "column_3": "summary",
    "column_4": "plot",
})
# Query the graph to check what we have
print("---\nHere are the actors and the characters they played in Interstellar:")
res = conn.execute(
    """
    MATCH (a:Actor)-[:ACTED_IN]->(m:Movie {title: "Interstellar"}),
          (a)-[:PLAYED]->(c:Character)
    RETURN DISTINCT a.name, c.name
    """
)
while res.has_next():
    data = res.get_next()
    print(f"{data[0]} -> {data[1]}")
