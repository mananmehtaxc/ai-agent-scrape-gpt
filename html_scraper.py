import requests
from bs4 import BeautifulSoup

def scrape_html(url):
    """
    Scrape the HTML content of a given URL and return the text content.
    
    Args:
        url (str): The URL to scrape.
        
    Returns:
        str: The text content of the HTML page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        # Remove script and style elements
        for script_or_style in soup(['script', 'style', "nav", "footer", "header"]):
            script_or_style.decompose()
        # Get the text content
        soup = soup.get_text(separator=' ', strip=True)
        # Normalize whitespace
        soup = ' '.join(soup.split())
        return soup.get_text()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None 