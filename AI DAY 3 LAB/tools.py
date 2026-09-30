import os
from bs4 import BeautifulSoup


def read_notice():
    """Read and return the college fee notice."""

    file_path = os.path.join(
        os.path.dirname(__file__),
        "notice.html"
    )

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(" ", strip=True)

    except Exception as e:
        return f"Error reading notice: {e}"