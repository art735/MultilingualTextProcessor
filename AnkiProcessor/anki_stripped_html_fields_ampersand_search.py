import re
import requests
from bs4 import BeautifulSoup


ANKICONNECT_URL = "http://127.0.0.1:8765"

# Пустой запрос = все карточки.
# ANKI_QUERY = ""

# Можно ограничить по названию колоды:
# ANKI_QUERY = 'deck:"German"'
# ANKI_QUERY = 'deck:"German::B2"'
# ANKI_QUERY = 'deck:"German::B2"'

# Можно ограничить по названию note type:
ANKI_QUERY = 'note:"Basic (and reversed card) (with additional fields)"'

# Название поля, в котором осуществляется поиск
# FIELD_NAME = "Back"

# Что именно ищем в очищенном от HTML тексте.
# [A-Za-z]+ = одна или более английских букв подряд.
# PATTERN = re.compile(r"[A-Za-z]{2,}")
PATTERN = re.compile("&")

# Английские последовательности, которые не должны считаться результатом поиска.
ALLOWED_AMPERSAND_WORDS = {

}


# Сколько карточек запрашивать за один cardsInfo.
BATCH_SIZE = 5000


def invoke(action, **params):
    """Вызов AnkiConnect API."""
    response = requests.post(
        ANKICONNECT_URL,
        json={
            "action": action,
            "version": 6,
            "params": params,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("error") is not None:
        raise RuntimeError(f"AnkiConnect error: {data['error']}")

    return data["result"]


def html_to_visible_text(html):
    """
    Преобразует HTML поля в видимый текст.

    Inline-теги (<b>, <span>, <i> и т. п.) не разделяют слова:
        <b>hel</b><span>lo</span> -> hello

    Некоторые невидимые элементы удаляются.
    """
    soup = BeautifulSoup(html or "", "html.parser")

    # Эти элементы не относятся к видимому тексту карточки.
    for tag in soup(["script", "style", "noscript", "template"]):
        tag.decompose()

    # <br> превращаем в пробел.
    for tag in soup.find_all("br"):
        tag.replace_with(" ")

    # Получаем текст без HTML-тегов.
    text = soup.get_text(separator="", strip=True)

    # Нормализуем пробелы.
    text = re.sub(r"\s+", " ", text)

    return text


def chunks(sequence, size):
    """Разбивает список на небольшие части."""
    for i in range(0, len(sequence), size):
        yield sequence[i:i + size]


def main():
    # 1. Получаем ID всех нужных карточек.
    card_ids = invoke("findCards", query=ANKI_QUERY)

    print(f"Всего карточек для проверки: {len(card_ids)}")

    matched_ids = []

    # 2. Получаем информацию о карточках порциями.
    for batch in chunks(card_ids, BATCH_SIZE):
        cards = invoke("cardsInfo", cards=batch)

        for card in cards:
            for field_name in card["fields"].keys():
                if field_name in ["Front", "Transcription", "Back"]:
                    field_html = card["fields"][field_name]["value"]

                    # 3. Убираем HTML и оставляем видимый текст.
                    field_plain_text = html_to_visible_text(field_html)

                    # 4. Ищем английские буквы.
                    found_words = PATTERN.findall(field_plain_text.lower())

                    if not found_words:
                        continue

                    # Интересуют только те карточки, в которых встречаются
                    # английские слова, отсутствующие в списке слов-исключений
                    unexpected_words = [
                        word
                        for word in found_words
                        if word not in ALLOWED_AMPERSAND_WORDS
                    ]

                    if unexpected_words:
                        matched_ids.append(card["cardId"])

    # 5. Удаляем возможные дубликаты и сохраняем порядок.
    matched_ids = list(dict.fromkeys(matched_ids))

    # Формат непосредственно для Anki Browser:
    anki_query = "cid:" + ",".join(map(str, matched_ids))

    print(f"\nНайдено карточек: {len(matched_ids)}\n")

    print("\nГОТОВЫЙ ЗАПРОС ДЛЯ ANKI:")
    print(anki_query)

    # Открываем результаты в Anki Browser
    invoke("guiBrowse", query=anki_query)


if __name__ == "__main__":
    main()
