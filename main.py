import requests
from bs4 import BeautifulSoup

base_url = "https://habr.com"

def get_links(page_number, query):
    search_url = f"{base_url}/ru/search/page{page_number}/?q={query}&target_type=posts&order=relevance"
    request = requests.get(search_url)

    links = []
    soup = BeautifulSoup(request.content, "html.parser")
    articles = soup.find_all("article")
    for article in articles:
        link = article.find("a", class_="tm-title__link")["href"]
        links.append(link)
    return links


def get_page_content(url):
    request = requests.get(url)
    return request.text


def save_pages(links):
    index_entries = []
    for idx, link in enumerate(links):
        with open(f'saved_pages/page{idx}.txt', 'w', encoding='utf-8') as f:
            f.write(get_page_content(base_url + link))
        index_entries.append(f'page{idx}.txt - {base_url + link}')

    with open('index.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_entries))


def main():
    page_number = 1
    all_links = []
    while len(all_links) < 100:
        links = get_links(page_number=page_number, query="kotlin")
        all_links.extend(links)
        page_number += 1
    save_pages(all_links)


if __name__ == "__main__":
    main()
