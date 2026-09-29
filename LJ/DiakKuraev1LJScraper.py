import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class DiakKuraev1LJScraper:
    BASE_URL = "https://diak-kuraev1.livejournal.com"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    def __init__(self, start_date, end_date, output_html=None):
        self.start_date = start_date
        self.end_date = end_date

        # Если имя файла не передано, формируем его автоматически:
        # kuraev_posts_month_year.html (например, kuraev_posts_december2025.html)
        if output_html is None:
            month_name = self.start_date.strftime("%B").lower()
            self.output_html = f"kuraev_posts_{month_name}{self.start_date.year}.html"
        else:
            self.output_html = output_html

        self.articles = []

    def scrape(self):
        current_date = self.start_date
        while current_date <= self.end_date:
            url = f"{self.BASE_URL}/{current_date.strftime('%Y/%m/%d')}/"
            print(f"📅 Скачивание: {url}")
            try:
                resp = requests.get(url, headers=self.HEADERS, timeout=10)
                resp.raise_for_status()
            except Exception as e:
                print(f"⚠️ Ошибка при загрузке {url}: {e}")
                current_date += timedelta(days=1)
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            articles = soup.find_all("article")

            # В блоге LiveJournal посты могут быть свёрнуты с помощью механизма lj-cut.
            # В этом случае <article> содержит только часть текста, а полный текст доступен по ссылке вроде:
            # <a href="https://diak-kuraev1.livejournal.com/77421.html#cutid1" class="ljcut-link-expand">
            # Для получения постов в "развёрнутом" виде нужно сделать следующее:
            # 1. На странице дня (YYYY/MM/DD) собрать все <article>-элементы.
            # 2. Проверить, есть ли внутри <article> тег <a class="ljcut-link-expand">.
            # 3. Если да — извлечь ссылку href и сделать отдельный запрос по ней, чтобы получить полный текст.
            # 4. Заменить <article> из "дневной" страницы на <article> из полной страницы.
            for article in articles:
                full_article = self._expand_if_cut(article)
                self.articles.append(str(full_article))

            current_date += timedelta(days=1)

    def _expand_if_cut(self, article_tag):
        """Загружает полную версию поста, если есть lj-cut, и очищает <article> от следующих элементов:
          - div.entryunit__userpic
          - footer.entryunit__footer"""
        cut_link = article_tag.select_one("a.ljcut-link-expand")
        full_article = article_tag

        if cut_link:
            href = cut_link.get("href")
            if href:
                if not href.startswith("http"):
                    href = self.BASE_URL + href
                print(f" → Развёртывание: {href}")
                try:
                    resp = requests.get(href, headers=self.HEADERS, timeout=10)
                    resp.raise_for_status()
                    soup = BeautifulSoup(resp.text, "html.parser")
                    fetched_article = soup.find("article")
                    if fetched_article:
                        full_article = fetched_article
                except Exception as e:
                    print(f"   ⚠️ Ошибка при загрузке полного поста: {e}")

        # Удаляем userpic
        userpic = full_article.select_one("div.entryunit__userpic")
        if userpic:
            userpic.decompose()

        # Удаляем footer
        footer = full_article.select_one("footer.entryunit__footer")
        if footer:
            footer.decompose()

        return full_article

    def save_html(self):
        joined = "<hr/>\n".join(self.articles)
        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Архив постов Кураева</title>
</head>
<body>
    {joined}
</body>
</html>
"""
        with open(self.output_html, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n✅ Сохранено {len(self.articles)} постов в файл: {self.output_html}")


#####################################

# Порядок работы:
# 1. Включить desktop-ный (но не браузерный!) VPN (например, ProtonVPN)
# 2. Выставить диапазон дат, за которые нужно собрать посты в LJ
# 3. Запустить скрипт

if __name__ == '__main__':
    scraper = DiakKuraev1LJScraper(
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 1, 7)
    )

    scraper.scrape()
    scraper.save_html()