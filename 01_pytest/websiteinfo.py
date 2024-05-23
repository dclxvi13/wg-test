import re
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class WebsiteInfo:
    name: str
    frontend: str
    backend: str
    visitors_per_month: int
    database: str


URL = "https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites"


def extract_int_from_string(text: str) -> int:
    numbers = re.findall(r'\d+', text)
    return int(''.join(numbers))


def remove_references(text: str) -> str:
    """Удаляет сноски вида [2], [12], [123] и т.д."""
    return re.sub(r'\[\d+\]', '', text)


def get_website_data():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')[1:]  # Пропускаем заголовок

    websites = []

    for row in rows:
        cols = row.find_all('td')
        name = remove_references(cols[0].get_text(strip=True))
        visitors_str = remove_references(cols[1].get_text(strip=True).replace(',', ''))
        visitors_per_month = extract_int_from_string(visitors_str)
        frontend = remove_references(cols[2].get_text(strip=True))
        backend = remove_references(cols[3].get_text(strip=True))
        database = remove_references(cols[4].get_text(strip=True))

        websites.append(
            WebsiteInfo(name=name,
                        frontend=frontend,
                        backend=backend,
                        visitors_per_month=visitors_per_month,
                        database=database))

    return websites
