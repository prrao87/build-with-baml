""""
Use the results from the BAML workflow to compare the performance of the LLMs and the rule-based API.
"""
import polars as pl
from typing import Tuple, Optional, Dict, List


def load_datasets(
    hand_annotated_path: str = "../../data/nobel_laureates/hand_annotated/unknown_scholars.csv",
    genderapi_path: str = "../../data/nobel_laureates/with_gender/scholars_from_genderapi.jsonl",
    llm1_path: str = "../../data/nobel_laureates/with_gender/scholars_from_baml_gpt-4o-mini.jsonl",
    llm2_path: str = "../../data/nobel_laureates/with_gender/scholars_from_baml_gemma3_12b.jsonl",
    llm3_path: str = "../../data/nobel_laureates/with_gender/scholars_from_baml_gemma3_27b.jsonl"
) -> Dict[str, pl.DataFrame]:
    """Load all datasets."""
    datasets = {
        "Hand-annotated": pl.read_csv(hand_annotated_path),
        "GenderAPI": pl.read_ndjson(genderapi_path),
        "GPT-4o-mini": pl.read_ndjson(llm1_path),
        "Gemma3-12b": pl.read_ndjson(llm2_path),
        "Gemma3-27b": pl.read_ndjson(llm3_path)
    }
    return datasets


def calculate_accuracy(
    reference_df: pl.DataFrame, 
    model_df: pl.DataFrame, 
    join_col: str = "name",
    ref_gender_col: str = "gender", 
    model_gender_col: str = "gender"
) -> Tuple[float, int, int, Optional[pl.DataFrame]]:
    """Calculate accuracy between reference and model datasets."""
    # Join the datasets
    comparison_df = reference_df.join(model_df, on=join_col, how="inner")
    
    # Calculate accuracy
    total_matches = len(comparison_df)
    correct_predictions = comparison_df.filter(pl.col(f"{ref_gender_col}") == pl.col(f"{model_gender_col}_right")).height
    accuracy = (correct_predictions / total_matches) * 100 if total_matches > 0 else 0
    
    # Find mismatches
    mismatches = comparison_df.filter(pl.col(f"{ref_gender_col}") != pl.col(f"{model_gender_col}_right"))
    
    return accuracy, correct_predictions, total_matches, mismatches


def compare_all_models(datasets: Dict[str, pl.DataFrame]) -> List[Dict]:
    """Compare all models against the reference dataset."""
    reference_df = datasets["Hand-annotated"]
    results = []
    
    for model_name, model_df in datasets.items():
        if model_name == "Hand-annotated":
            continue
            
        accuracy, correct, total, mismatches = calculate_accuracy(
            reference_df, 
            model_df,
            ref_gender_col="gender",
            model_gender_col="gender"
        )
        
        results.append({
            "Model": model_name,
            "Accuracy": accuracy,
            "Correct": correct,
            "Total": total,
            "Mismatches": mismatches
        })
    
    return results


def print_table(results: List[Dict]) -> None:
    """Print a formatted table of results."""
    print(f"{'Model':<15} {'Accuracy':<10} {'Correct/Total':<15}")
    print("-" * 45)
    
    for result in results:
        print(
            f"{result['Model']:<15} "
            f"{result['Accuracy']:.2f}%{' ':>5} "
            f"{result['Correct']}/{result['Total']}"
        )
    
    print("-" * 45)


def print_detailed_results(
    results: List[Dict],
    show_mismatches: bool = False
) -> None:
    """Print detailed results for each model."""
    for result in results:
        print(f"\n{result['Model']} Results:")
        print(f"  Accuracy: {result['Accuracy']:.2f}%")
        print(f"  Correct predictions: {result['Correct']} out of {result['Total']}")
        
        if show_mismatches and result['Mismatches'] is not None and len(result['Mismatches']) > 0:
            print(f"\n  Mismatches for {result['Model']}:")
            print(result['Mismatches'].select(["name", "gender", "gender_right"]))


def main(show_mismatches: bool = False):
    """
    Main function to evaluate model accuracy.
    
    Args:
        show_mismatches: Whether to print mismatches
    """
    # Load all datasets
    datasets = load_datasets()
    
    # Calculate accuracy for all models
    results = compare_all_models(datasets)
    
    # Print summary table
    print("\nAccuracy comparison for unknown genders across all results:")
    print_table(results)
    
    # Print detailed results
    if show_mismatches:
        print_detailed_results(results, show_mismatches=True)


if __name__ == "__main__":
    # Set to True to show mismatches
    main(show_mismatches=False)


