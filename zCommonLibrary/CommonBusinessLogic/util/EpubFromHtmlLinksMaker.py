import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from ebooklib import epub
import time

BASE_URL = 'https://developer.mozilla.org'
START_PATH = '/en-US/docs/Web/JavaScript/Guide'
START_URL = BASE_URL + START_PATH
SAVE_FOLDER = r'f:\mdn_js_guide'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; MDN_EPUB_Bot/1.0)'
}

# Создаём папку для сохранения HTML
os.makedirs(SAVE_FOLDER, exist_ok=True)

def get_html(url):
    print(f'Fetching {url}')
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.text

def save_html(filename, content):
    path = os.path.join(SAVE_FOLDER, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def load_html(filename):
    path = os.path.join(SAVE_FOLDER, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def is_guide_url(url):
    # Проверяем, что URL в пределах /en-US/docs/Web/JavaScript/Guide
    parsed = urlparse(url)
    return parsed.path.startswith(START_PATH)

def sanitize_filename(url):
    # Преобразуем URL в имя файла, например /en-US/docs/Web/JavaScript/Guide/Loops -> Loops.html
    name = url.rstrip('/').split('/')[-1]
    if not name:
        name = 'index'
    return name + '.html'

def crawl_guide():
    # Очередь URL для обхода и множество уже посещённых
    to_visit = {START_URL}
    visited = set()

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        try:
            html = get_html(url)
        except Exception as e:
            print(f'Error fetching {url}: {e}')
            continue

        filename = sanitize_filename(url)
        save_html(filename, html)

        visited.add(url)

        # Парсим и ищем ссылки внутри статьи
        soup = BeautifulSoup(html, 'html.parser')

        article = soup.find('article', id='content')
        if not article:
            article = soup.body

        if article:
            links = article.find_all('a', href=True)
            for a in links:
                href = a['href']
                full_url = urljoin(BASE_URL, href)
                if is_guide_url(full_url) and full_url not in visited and full_url not in to_visit:
                    to_visit.add(full_url)

        # Чтобы не нагружать сервер, пауза 1 секунда
        time.sleep(1)

    print(f'Total pages downloaded: {len(visited)}')
    return visited

def build_epub():
    book = epub.EpubBook()
    book.set_title('JavaScript Guide - MDN')
    book.set_language('en')

    files = sorted(os.listdir(SAVE_FOLDER))
    chapters = []

    for i, filename in enumerate(files):
        if not filename.endswith('.html'):
            continue
        html = load_html(filename)
        soup = BeautifulSoup(html, 'html.parser')

        content = soup.find('article', id='content')
        if content is None:
            content = soup.body

        title = soup.title.string if soup.title else f'Chapter {i+1}'

        chapter = epub.EpubHtml(title=title, file_name=f'chap_{i+1}.xhtml', lang='en')
        chapter.content = str(content)
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ['nav'] + chapters

    epub.write_epub('MDN_JavaScript_Guide.epub', book)
    print('EPUB файл создан: MDN_JavaScript_Guide.epub')

def main():
    crawl_guide()
    build_epub()

if __name__ == '__main__':
    main()
