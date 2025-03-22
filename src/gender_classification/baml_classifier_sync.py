"""
Use BAML to call an LLM API to get gender for a full name.

Run synchronously, so this will be slower than the async version and can be used
for slower API servers or during the debugging stage.
"""

import argparse
import asyncio
import json
import os
from itertools import islice
from pathlib import Path

from baml_client import b, reset_baml_env_vars
from dotenv import load_dotenv
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn

load_dotenv()
os.environ["BAML_LOG"] = "WARN"
reset_baml_env_vars(dict(os.environ))


async def process_scholar(scholar, output_file, error_log_file):
    try:
        # format the scholar info for the LLM
        if scholar.get("category") and scholar.get("year"):
            info = f"name: {scholar['name']}\ninfo: {scholar['year']} {scholar['category']} nobel prize"
        else:
            info = f"name: {scholar['name']}\ninfo: scholar"
        result = b.ClassifyGender(info)
        scholar["gender"] = result.value.lower()

        # Write result to file
        with open(output_file, "a") as f:
            f.write(json.dumps(scholar) + "\n")

        return True
    except Exception as e:
        # Log errors to a separate file
        with open(error_log_file, "a") as f:
            f.write(f"Error processing {scholar['name']}: {str(e)}\n")
        return False


async def process_batch(batch, output_file, error_log_file, progress, task):
    tasks = [process_scholar(scholar, output_file, error_log_file) for scholar in batch]
    results = await asyncio.gather(*tasks)
    progress.update(task, advance=len(results))
    return results


async def main_async(data_path: Path, output_path: Path, limit: int | None) -> None:
    with open(data_path / "scholars.json", "r") as f:
        scholars: list[dict] = json.load(f)

    # Limit the number of scholars if specified
    if limit:
        scholars = scholars[:limit]

    # Output file
    output_file = output_path / "scholars_from_baml_gemma3_27b.jsonl"
    error_log_file = output_path / "error_log.txt"

    # Process with rich progress bar
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("[green]Processing scholars...", total=len(scholars))

        # Process in batches of 4
        batch_size = 4
        for i in range(0, len(scholars), batch_size):
            batch = scholars[
                i : i + batch_size
            ]  # This handles the final incomplete batch automatically
            await process_batch(batch, output_file, error_log_file, progress, task)

    print(f"\nProcessing complete. Results saved to {output_file}")


def main(data_path: Path, output_path: Path, limit: int | None) -> None:
    asyncio.run(main_async(data_path, output_path, limit))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process scholars data to add gender information")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of scholars to process (if none, all are processed)",
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=Path("../../data/nobel_laureates/"),
        help="Path to the directory containing scholars.json",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=None,
        help="Path to save the output",
    )

    args = parser.parse_args()

    data_path = args.data_path
    output_path = args.output_path if args.output_path else data_path / "predicted"
    output_path.mkdir(parents=True, exist_ok=True)

    main(data_path, output_path, args.limit)
