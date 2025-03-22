""" "
Use the results from the BAML workflow to compare the performance of the LLMs and the rule-based API.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import polars as pl


def load_datasets(
    reference_path: str,
    genderapi_path: str,
    llm1_path: str,
    llm2_path: str,
    llm3_path: str,
) -> Dict[str, pl.DataFrame]:
    """Load all datasets."""
    datasets = {
        "Hand-annotated": pl.read_csv(reference_path),
        "GenderAPI": pl.read_ndjson(genderapi_path),
        "GPT-4o-mini": pl.read_ndjson(llm1_path),
        "Gemma3-12b": pl.read_ndjson(llm2_path),
        "Gemma3-27b": pl.read_ndjson(llm3_path),
    }
    return datasets


def calculate_accuracy(
    reference_df: pl.DataFrame, model_df: pl.DataFrame, category: Optional[str] = None
) -> Tuple[float, int, int]:
    """
    Calculate accuracy for female laureate identification.

    Returns:
        Tuple of (accuracy percentage, model count, reference count)
    """
    # Filter by category if specified
    if category:
        reference_df = reference_df.filter(pl.col("category") == category)
        model_df = model_df.filter(
            (pl.col("category") == category)
            & (pl.col("gender") == "female")
            & (pl.col("type") == "laureate")
        )
    else:
        model_df = model_df.filter((pl.col("gender") == "female") & (pl.col("type") == "laureate"))

    # Get counts
    reference_count = reference_df.shape[0]
    model_count = model_df.shape[0]

    # Calculate accuracy as percentage of reference count
    accuracy = (model_count / reference_count * 100) if reference_count > 0 else 0

    return accuracy, model_count, reference_count


def print_category_table(datasets: Dict[str, pl.DataFrame], categories: List[str]) -> None:
    """Print table of results by category with relative counts."""
    print(
        f"{'Category':<25} {'GenderAPI':<15} {'gpt-4o-mini':<15} {'gemma3-12b':<15} {'gemma3-27b':<15}"
    )
    print("-" * 85)

    for category in categories:
        # Get reference count
        reference_df = datasets["Hand-annotated"].filter(pl.col("category") == category)
        reference_count = reference_df.shape[0]

        # Get model counts
        genderapi_count = (
            datasets["GenderAPI"]
            .filter(
                (pl.col("category") == category)
                & (pl.col("gender") == "female")
                & (pl.col("type") == "laureate")
            )
            .shape[0]
        )

        llm1_count = (
            datasets["GPT-4o-mini"]
            .filter(
                (pl.col("category") == category)
                & (pl.col("gender") == "female")
                & (pl.col("type") == "laureate")
            )
            .shape[0]
        )

        llm2_count = (
            datasets["Gemma3-12b"]
            .filter(
                (pl.col("category") == category)
                & (pl.col("gender") == "female")
                & (pl.col("type") == "laureate")
            )
            .shape[0]
        )

        llm3_count = (
            datasets["Gemma3-27b"]
            .filter(
                (pl.col("category") == category)
                & (pl.col("gender") == "female")
                & (pl.col("type") == "laureate")
            )
            .shape[0]
        )

        # Print comparison with relative counts
        print(
            f"{category:<25} "
            f"{genderapi_count}/{reference_count:<14} "
            f"{llm1_count}/{reference_count:<14} "
            f"{llm2_count}/{reference_count:<14} "
            f"{llm3_count}/{reference_count:<14}"
        )

    print("-" * 85)


def print_accuracy_table(
    datasets: Dict[str, pl.DataFrame], categories: Optional[List[str]] = None
) -> None:
    """Print count comparison table similar to eval_unknown.py."""
    reference_df = datasets["Hand-annotated"]

    # Calculate counts for each model
    results = []
    for model_name, model_df in datasets.items():
        if model_name == "Hand-annotated":
            continue

        _, model_count, reference_count = calculate_accuracy(reference_df, model_df)

        results.append({"Model": model_name, "Count": model_count, "Reference": reference_count})

    # Print the table
    print("\nFemale laureate identification counts:")
    print(f"{'Model':<15} {'Predicted/Hand-annotated':<15}")
    print("-" * 35)

    for result in results:
        print(f"{result['Model']:<15} " f"{result['Count']}/{result['Reference']}")

    print("-" * 35)

    # Print per-category counts if categories provided
    if categories:
        print("\nCounts by category:")
        for category in categories:
            print(f"\n{category}:")
            print(f"{'Model':<15} {'Predicted/Hand-annotated':<25}")
            print("-" * 45)

            for model_name, model_df in datasets.items():
                if model_name == "Hand-annotated":
                    continue

                _, model_count, reference_count = calculate_accuracy(
                    reference_df, model_df, category=category
                )

                print(f"{model_name:<15} " f"{model_count}/{reference_count}")

            print("-" * 45)


def print_female_laureates_by_category(
    datasets: Dict[str, pl.DataFrame], categories: List[str]
) -> None:
    """Print the names of female laureates identified by each method in each category."""
    print("\n==== Female Laureates by Category ====")

    for category in categories:
        print(f"\n## {category} ##")

        # Get reference names
        reference_df = datasets["Hand-annotated"].filter(pl.col("category") == category)
        reference_names = reference_df["name"].to_list()

        print(f"\nHand-annotated ({len(reference_names)}):")
        for name in sorted(reference_names):
            print(f"  {name}")

        # Print names identified by each model
        for model_name, model_df in datasets.items():
            if model_name == "Hand-annotated":
                continue

            female_laureates = model_df.filter(
                (pl.col("category") == category)
                & (pl.col("gender") == "female")
                & (pl.col("type") == "laureate")
            )

            model_names = female_laureates["name"].to_list()

            # Find names that were incorrectly predicted (not in reference)
            incorrect_predictions = [name for name in model_names if name not in reference_names]
            # Find names that were missed (in reference but not predicted)
            missed_predictions = [name for name in reference_names if name not in model_names]

            print(f"\n{model_name} ({len(model_names)}):")
            for name in sorted(model_names):
                if name not in reference_names:
                    print(f"  {name} [INCORRECT]")
                else:
                    print(f"  {name}")

            if missed_predictions:
                print(f"\n  {model_name} missed these laureates:")
                for name in sorted(missed_predictions):
                    print(f"  - {name}")


def compare_gender_results(
    reference_path: str,
    genderapi_path: str,
    llm1_path: str,
    llm2_path: str,
    llm3_path: str,
    categories: Optional[List[str]] = None,
    print_names: bool = False,
) -> None:
    """
    Compare gender identification results between reference data, rule-based API, and LLM.

    Args:
        reference_path: Path to the reference CSV with hand-annotated female laureates
        genderapi_path: Path to the rule-based API results (JSONL)
        llm1_path: Path to the first LLM results (JSONL)
        llm2_path: Path to the second LLM results (JSONL)
        llm3_path: Path to the third LLM results (JSONL)
        categories: List of categories to compare (defaults to Physics, Chemistry, etc.)
        print_names: Whether to print individual laureate names
    """
    if categories is None:
        categories = ["Physics", "Chemistry", "Physiology or Medicine", "Economic Sciences"]

    # Load all datasets
    datasets = load_datasets(reference_path, genderapi_path, llm1_path, llm2_path, llm3_path)

    # Print the original category table
    print("Female laureate counts by category:")
    print_category_table(datasets, categories)

    # Print the new accuracy table
    print_accuracy_table(datasets, categories)

    # Print individual laureate names if requested
    if print_names:
        print_female_laureates_by_category(datasets, categories)


if __name__ == "__main__":
    compare_gender_results(
        reference_path="../../data/nobel_laureates/human_annotated/female_laureates_until_2022.csv",
        genderapi_path="../../data/nobel_laureates/predicted/scholars_from_genderapi.jsonl",
        llm1_path="../../data/nobel_laureates/predicted/scholars_from_baml_gpt-4o-mini.jsonl",
        llm2_path="../../data/nobel_laureates/predicted/scholars_from_baml_gemma3_12b.jsonl",
        llm3_path="../../data/nobel_laureates/predicted/scholars_from_baml_gemma3_27b.jsonl",
        print_names=True,  # Enable printing of individual names
    )
