# Classification

## Goal

The goal is to use BAML to classify a movie based on its title and plot, into up to 3 genres.
This is a multi-label classification problem.

See the list of movie plots in `../../data/movie_plots`.

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
uv run run_baml.py
```

This will output the following:

```console
Dunkirk: ['War', 'Drama', 'Thriller']
Interstellar (film): ['SciFi', 'Drama', 'Mystery']
Prometheus: ['SciFi', 'Horror', 'Mystery']
The Lunchbox: ['Romance', 'Drama']
Inception (film): ['SciFi', 'Thriller', 'Drama']
```