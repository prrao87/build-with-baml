"""
Use RapidAPI to call gender-api.com to get gender for a full name.
"""

import argparse
import asyncio
import json
import os
from pathlib import Path

import aiohttp
from dotenv import load_dotenv
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

load_dotenv()

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")
assert RAPIDAPI_KEY, "RAPIDAPI_KEY is not set"


async def get_gender(full_name: str, session: aiohttp.ClientSession) -> str:
    """Get gender for a full name using RapidAPI."""
    url = "https://gender-api-com.p.rapidapi.com/gender/by-full-name"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "gender-api-com.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY,
    }
    payload = {"full_name": full_name}

    try:
        async with session.post(url, headers=headers, json=payload) as response:
            result = await response.json()
            print(f"API Response for {full_name}: {result}")  # Debug the full response
            gender = result.get("gender", "unknown")
            if gender is None:
                print(f"Got None gender for {full_name}. Full response keys: {result.keys()}")
            return gender or "unknown"
    except Exception as e:
        print(f"Error getting gender for {full_name}: {e}")
        return "unknown"


async def process_batch(scholars: list, session: aiohttp.ClientSession, progress, task) -> list:
    """Process a batch of scholars concurrently"""
    tasks = []
    for scholar in scholars:
        if "name" in scholar and "gender" not in scholar:
            tasks.append(asyncio.create_task(get_gender(scholar["name"], session)))
        else:
            tasks.append(asyncio.create_task(asyncio.sleep(0)))

    results = await asyncio.gather(*tasks)

    for scholar, gender in zip(scholars, results):
        if "name" in scholar and "gender" not in scholar:
            scholar["gender"] = gender
        progress.update(task, advance=1)

    return scholars


async def main(data_path: Path, output_path: Path, limit: int) -> None:
    if not limit:
        limit = 10000

    with open(data_path / "scholars.json", "r", encoding="utf-8") as f:
        scholars = json.load(f)

    if limit:
        scholars = scholars[:limit]

    BATCH_SIZE = 10  # Adjust based on API limits

    async with aiohttp.ClientSession() as session:
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("[green]Processing names...", total=len(scholars))

            # Process scholars in batches
            processed_scholars = []
            for i in range(0, len(scholars), BATCH_SIZE):
                batch = scholars[i : i + BATCH_SIZE]
                processed_batch = await process_batch(batch, session, progress, task)
                processed_scholars.extend(processed_batch)
                # await asyncio.sleep(0.1)  # Rate limiting

    # Save the updated data
    with open(output_path / "scholars_from_genderapi.jsonl", "w", encoding="utf-8") as f:
        for scholar in processed_scholars:
            f.write(json.dumps(scholar, ensure_ascii=False) + "\n")

    print(
        f"Processed {len(processed_scholars)} scholars and saved to scholars_from_genderapi.jsonl"
    )


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

    asyncio.run(main(data_path, output_path, args.limit))
