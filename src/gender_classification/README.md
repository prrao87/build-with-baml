# Classification

## Goal

We will use BAML to prompt multiple LLMs and classify the gender of a dataset of scholars and Nobel laureates.
We will compare the performance of 3 LLMs (`gpt-4o-mini`, `gemma3-12b`, `gemma3-27b`) vs. a
gender prediction API ([gender-api.com](https://gender-api.com/)) and see if BAML + an LLM can help with
classification tasks.

See the list of scholars in [`../../data/nobel_laureates/scholars.json`](../../data/nobel_laureates/scholars.json). If the `type` if specified as `"laureate"`,
they are Nobel laureates, while the rest are scholars who mentored the laureates
or influenced them in some way. The dataset is obtained from [this source](https://github.com/rtol/NobelNetwork) repo, which models the
mentorshop tree of the Nobel laureates as a graph.

Because no gender information is provided in the original dataset, we will define
and run this as a classification task!

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
# Useful if you have slow inference due to hardware or LLM API rate limitations
uv run baml_classifier_sync.py
```

Similarly, you can run the gender prediction API script as follows:
```bash
uv run gender_classifier_async.py
```

## Evaluation

Human-annotated data is provided in CSV format for a select set of scholars [here](../../data/nobel_laureates/human_annotated). The goal is to compare the performance of the LLMs and
the gender prediction API on the human-annotated data.

There are three evaluation scripts to run:

1. `eval_female_laureates.py`: Evaluate the performance of the LLM and the gender prediction API on female laureates.
2. `eval_random_scholars.py`: Evaluate the performance of the LLM and the gender prediction API on random scholars.
3. `eval_unknown.py`: Evaluate the performance of the LLM and the gender prediction API on scholars with unknown gender.

Run the evaluation scripts as follows:
```bash
uv run eval_female_laureates.py
uv run eval_random_scholars.py
uv run eval_unknown.py
```

See the [blog post](https://thedataquarry.com/blog/using-llms-to-enrich-datasets) for a deep
dive into the evaluation results.



