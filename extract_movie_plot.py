"""
Extract the plots of movies from Wikipedia.

The plots are strings that are stored in the `data/movie_plots` directory.
"""

from pathlib import Path
from typing import Optional

import wikipedia


def extract_movie_plot(title: str) -> Optional[str]:
    try:
        # Get the Wikipedia page
        page = wikipedia.page(title, auto_suggest=False)

        # Find the plot section
        content = page.content
        sections = content.split("== Plot ==")
        if len(sections) < 2:
            sections = content.split("==Plot==")

        if len(sections) < 2:
            return None

        # Extract plot section (stops at next section)
        plot = sections[1].split("==")[0].strip()
        plot = plot.replace("\n", " ")  # Replace newlines with spaces

        return plot

    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Disambiguation error: {e.options}")
        return None
    except wikipedia.exceptions.PageError:
        print(f"Page not found for {title}")
        return None


if __name__ == "__main__":
    movies = [
        # "Interstellar (film)",
        # "Dunkirk (2017 film)",
        # "Inception (film)",
        # "Prometheus (2012 film)",
        "The Lunchbox"
    ]
    for movie in movies:
        plot = extract_movie_plot(movie)
        # Output the plots to files so we can use them for RAG
        output_path = Path("data") / "movie_plots"
        output_path.mkdir(parents=True, exist_ok=True)
        if plot:
            with open(output_path / f"{movie}.txt", "w") as f:
                f.write(plot)
