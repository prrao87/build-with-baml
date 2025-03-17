# Classification

## Goal

The goal is to use BAML to classify the gender of a dataset of scholars and Nobel laureates.
We will compare the performance of 3 LLMs (`gpt-4o-mini`, `gemma3-12b`, `gemma3-27b`) vs. a
rule-based API ([gender-api.com](https://gender-api.com/)) and see if BAML + an LLM can help with
classification tasks.

See the list of people in [`../../data/nobel_laureates/scholars.json`](../../data/nobel_laureates/scholars.json). Scholars who are of the
type `'laureate'` are Nobel laureates, while the rest are scholars who mentored the laureates
or influenced them in some way. The dataset is obtained from [this source](https://github.com/rtol/NobelNetwork), which models the
mentorshop tree of the Nobel laureates as a graph. No gender information is provided in the original
dataset, which is the motivation behind this classification task!

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

Human-annotated data is provided for a select set of scholars [here](../../data/nobel_laureates/human_annotated). There are three evaluation scripts provided:

1. `eval_female_laureates.py`: Evaluate the performance of the LLM and the rule-based API on female laureates.
2. `eval_random_scholars.py`: Evaluate the performance of the LLM and the rule-based API on random scholars.
3. `eval_unknown.py`: Evaluate the performance of the LLM and the rule-based API on scholars with unknown gender.

Run the evaluation scripts as follows:
```bash
uv run eval_female_laureates.py
uv run eval_random_scholars.py
uv run eval_unknown.py
```



