import requests
from bs4 import BeautifulSoup

def scrape_html(url: str) -> str:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text.strip()
    except Exception as e:
        print(f"[Scraper] Error: {e}")
        return ""