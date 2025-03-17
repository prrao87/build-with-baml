# Classification

## Goal

The goal is to use BAML to classify the gender of a dataset of scholars and Nobel laureates.
We will compare the performance of an LLM (`gpt-4o-mini`) and a rule-based API (`genderapi.com`)
and see if BAML + an LLM can outperform the rule-based API.

See the list of scholars and Nobel laureates in `../../data/nobel_laureates/scholars.json`.

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

To run the script, you can run the BAML workflow that's defined in `run_baml.py`.
```bash
# Run the BAML workflow asynchronously
uv run baml_classifier_async.py

# (Optionally) run the BAML workflow synchronously
# Useful for debugging or when the LLM API is rate limited
uv run baml_classifier_sync.py
```

## Evaluate the performance of the LLM and the rule-based API

There are three evaluation scripts provided:    

1. `eval_female_laureates.py`: Evaluate the performance of the LLM and the rule-based API on female laureates.
2. `eval_random_scholars.py`: Evaluate the performance of the LLM and the rule-based API on random scholars.
3. `eval_unknown.py`: Evaluate the performance of the LLM and the rule-based API on scholars with unknown gender.

To run the evaluation scripts, you can run the following command:
```bash
uv run eval_female_laureates.py
uv run eval_random_scholars.py
uv run eval_unknown.py
```

More numbers on this coming soon!



