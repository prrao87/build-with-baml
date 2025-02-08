from __future__ import annotations

import re
from pathlib import Path
from typing import Generator

from baml_client import b


def get_titles_and_plots(file_path: str) -> Generator[tuple[str, str], None, None]:
    files = Path(file_path).glob("*.txt")
    for file in files:
        with open(file, "r") as f:
            title = file.stem
            # Remove patterns like (2017 film) and (film) from the title
            title = re.sub(r"\s*\((?:\d{4}.*?|film)\)", "", title)
            plot = f.read()
            yield title, plot


if __name__ == "__main__":
    file_path = "../../data/movie_plots/"
    for title, plot in get_titles_and_plots(file_path):
        result = b.ClassifyMovie(title, plot)
        labels = [label.value for label in result.genres]
        print(f"{title}: {labels}")
