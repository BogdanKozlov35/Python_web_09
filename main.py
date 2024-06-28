import requests
from bs4 import BeautifulSoup
import json
import os

import seed.seed


def get_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []
    authors_links = set()
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        author_link = quote.find('small', class_='author').find_next_sibling('a')['href']

        quotes.append({
            'quote': text,
            'author': author,
            'tags': tags
        })

        authors_links.add(author_link)

    return quotes, list(authors_links)


def get_authors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    authors = []
    for author in soup.find_all('div', class_='author-details'):
        fullname = author.find('h3', class_='author-title').text.strip()
        born_date = author.find('span', class_='author-born-date').text.strip()
        born_location = author.find('span', class_='author-born-location').text.strip()
        description = author.find('div', class_='author-description').text.strip()

        authors.append({
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        })

    return authors


def main():
    base_url = "http://quotes.toscrape.com"
    quotes = []
    authors = []
    author_urls = set()

    page_url = base_url

    while page_url:
        print(f"Scraping {page_url}")
        new_quotes, new_author_links = get_quotes(page_url)
        quotes.extend(new_quotes)
        author_urls.update(new_author_links)

        soup = BeautifulSoup(requests.get(page_url).text, 'html.parser')
        next_page = soup.find('li', class_='next')

        if next_page:
            page_url = base_url + next_page.find('a')['href']
        else:
            page_url = None

    for author_url in author_urls:
        full_author_url = base_url + author_url
        print(f"Scraping {full_author_url}")
        authors.extend(get_authors(full_author_url))

    with open('json/quotes.json', 'w') as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)

    with open('json/authors.json', 'w') as f:
        json.dump(authors, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
    seed.seed.main()