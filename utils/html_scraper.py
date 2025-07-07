import requests
from bs4 import BeautifulSoup

def scrape_html(url: str) -> str:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove irrelevant tags
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
            tag.decompose()

        # Extract and normalize text
        text = soup.get_text(separator="\n")
        cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        return cleaned_text

    except Exception as e:
        print(f"[Scraper] Error: {e}")
        return ""
