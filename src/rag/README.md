# RAG

## Goal

The goal is to use BAML to run traditional vector-based RAG. We will use LanceDB as the vector store.

## Setup

To sync the dependencies, run the following command:
```bash
# Assumes that the uv package manager is installed
# https://github.com/astral-sh/uv
uv sync
```

If you want to add more dependencies, you can do so as follows:
```bash
uv add <dependency>
```

## Run the workflow

To ingest the data into LanceDB and generate vector embeddings for the movie plots, run `ingest_data.py`.
```bash
uv run ingest_data.py
```

To execute the BAML workflow, run the code in `run_baml.py`.
```bash
uv run run_baml.py
```

This will output the following:

```console
title='Interstellar' question='Who does TARS primarily interface with in the movie Interstellar?' answer='TARS primarily interfaces with Cooper throughout the movie Interstellar.'
title='Interstellar' question="What is the special characteristic of Miller's planet in the movie Interstellar?" answer="Miller's planet experiences extreme time dilation, where a short period on the planet corresponds to a much longer period on the Endurance spacecraft."
```