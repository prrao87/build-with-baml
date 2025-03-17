"""
Use BAML to call an LLM API to get gender for a full name.

Runs asynchronously, so make sure to use an LLM API that supports concurrency.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from baml_client import reset_baml_env_vars
from baml_client.async_client import b  # Import the async client
from dotenv import load_dotenv
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeRemainingColumn

load_dotenv()
os.environ["BAML_LOG"] = "WARN"
reset_baml_env_vars(dict(os.environ))


async def process_batch(batch: List[Dict[str, Any]], output_file: Path, error_log_file: Path, progress, task) -> None:
    """Process a batch of scholars concurrently."""
    async def process_and_save(scholar: Dict[str, Any]) -> None:
        try:
            # Format the scholar info for the LLM
            if scholar.get("category") and scholar.get("year"): 
                info = f"name: {scholar['name']}\ninfo: {scholar['year']} {scholar['category']} nobel prize"
            else:
                info = f"name: {scholar['name']}\ninfo: scholar"
            
            # Call the LLM using the async client
            result = await b.ClassifyGender(info)
            scholar["gender"] = result.value.lower()
            
            # Write result to file
            with open(output_file, "a") as f:
                f.write(json.dumps(scholar) + "\n")
                
        except Exception as e:
            # Log errors to a separate file
            with open(error_log_file, "a") as f:
                f.write(f"Error processing {scholar['name']}: {str(e)}\n")
    
    # Process all scholars in the batch concurrently
    tasks = [process_and_save(scholar) for scholar in batch]
    await asyncio.gather(*tasks)
    
    # Update progress after batch completes
    progress.update(task, advance=len(batch))

async def main(data_path: Path, output_path: Path, limit: Optional[int], refresh: bool, batch_size: int) -> None:
    with open(data_path / "scholars.json", "r") as f:
        scholars: List[Dict[str, Any]] = json.load(f)

    # Limit the number of scholars if specified
    if limit:
        scholars = scholars[:limit]

    # Output file
    output_file = output_path / "scholars_from_baml_gemma3_27b_async.jsonl"
    error_log_file = output_path / "error_log.txt"
    
    # Delete existing file if refresh is True
    if refresh and output_file.exists():
        output_file.unlink()
        print(f"Deleted existing file: {output_file}")

    # Process with rich progress bar
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("[green]Processing scholars...", total=len(scholars))
        
        # Process in batches of specified size
        for i in range(0, len(scholars), batch_size):
            batch = scholars[i:i+batch_size]  # This handles the final incomplete batch automatically
            await process_batch(batch, output_file, error_log_file, progress, task)

    print(f"\nProcessing complete. Results saved to {output_file}")


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
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Delete existing output file before processing",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of scholars to process in each batch (default: 4)",
    )

    args = parser.parse_args()

    data_path = args.data_path
    output_path = args.output_path if args.output_path else data_path / "with_gender"
    output_path.mkdir(parents=True, exist_ok=True)

    asyncio.run(main(data_path, output_path, args.limit, args.refresh, args.batch_size))
