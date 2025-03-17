"""
Use RapidAPI to call gender-api.com to get gender for a full name.
"""

import argparse
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


def get_gender(full_name: str, session: requests.Session) -> str:
    """Get gender for a full name using RapidAPI."""
    url = "https://gender-api-com.p.rapidapi.com/gender/by-full-name"

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "gender-api-com.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY,
    }

    payload = {"full_name": full_name}

    try:
        response = session.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("gender", "unknown")
    except Exception as e:
        print(f"Error getting gender for {full_name}: {e}")
        return "unknown"


def main(data_path: Path, output_path: Path, limit: int) -> None:
    if not limit:
        limit = 10000
    # Load scholars data
    with open(data_path / "scholars.json", "r", encoding="utf-8") as f:
        scholars = json.load(f)

    # Create a session object for all requests
    session = requests.Session()

    # Process each scholar with rich progress bar
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("[green]Processing names...", total=len(scholars))

        for scholar in scholars[:limit]:
            if "name" in scholar and "gender" not in scholar:
                gender = get_gender(scholar["name"], session)
                scholar["gender"] = gender
                # Add a small delay to avoid rate limiting
                # time.sleep(0.1)
            progress.update(task, advance=1)

    # Save the updated data
    with open(output_path / "scholars_from_genderapi.jsonl", "w", encoding="utf-8") as f:
        for scholar in scholars:
            f.write(json.dumps(scholar, ensure_ascii=False) + "\n")

    print(f"Processed {len(scholars)} scholars and saved to scholars_from_genderapi.jsonl")


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
    output_path = args.output_path if args.output_path else data_path / "with_gender"
    output_path.mkdir(parents=True, exist_ok=True)

    main(data_path, output_path, args.limit)
