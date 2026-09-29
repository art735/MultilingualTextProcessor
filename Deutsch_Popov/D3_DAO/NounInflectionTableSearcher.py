import re

import requests
from bs4 import BeautifulSoup

base_url = "https://{lang}.wiktionary.org/wiki/"


# Gets noun inflection table from de.wikitonary.org
class NounInflectionTableSearcher:
    def __init__(self):
        pass

    def get_noun_inflection_tables(self, word):
        lang_code = 'de'
        word = word.capitalize()  # сделать существительное с большой буквы, для URL это имеет значение!!!
        url = base_url.format(lang=lang_code) + word

        response = requests.get(url)
        parser = 'html.parser'  # or lxml or html5lib
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None

        beautiful_soup = BeautifulSoup(response.content, parser, from_encoding=encoding)
        all_inflection_tables = beautiful_soup.find_all("table", class_="inflection-table")

        plural_regex = re.compile(
            r'Plural[\s\d]?')  # захватывает в шапке таблицы 'Plural', 'Plural 1', 'Plural 2', etc.
        # oblique case - косвенный падеж
        oblique_cases = ['Genitiv', 'Dativ', 'Akkusativ']

        results = list()
        for inflection_table in all_inflection_tables:
            raw_pieces = [piece for piece in re.split(r'\n', inflection_table.text) if piece]
            pieces = [i for i in raw_pieces if not (i == 'Singular' or plural_regex.match(i))]  # убрали шапку таблицы

            result = ""
            for piece in pieces:
                # если piece содержит 2 пробела (т. е. 3 элемента)
                # это возможно в следующих ситуациях: 'des Nachteilsdes Nachteiles', 'dem Nachteildem Nachteile'
                # это ситуации, когда артикль прилип к предыдущему слову и его нужно отделить!!!
                if len(piece.split()) == 3:
                    # positive lookbehind + rest of regexp
                    # искать de[sm], которое стояло бы НЕ перед пробелом и после него был пробел!
                    piece = re.sub(r'(?<=\S)de[sm]\s', ' / ' + r'\g<0>', piece)

                if piece not in oblique_cases:
                    result += (piece + '\t')
                else:
                    result += ('\n' + piece + '\t')

            # Разбиваем по newline, чтобы сделать strip торчащих справа знаков табуляции
            single_table_results = [res.strip() for res in result.split('\n')]
            result = '\n'.join(single_table_results)
            results.append(result)
        # loop end

        output = '\n*** ??? ***\n'.join(results)

        if output:
            return output
        else:
            return "!!! NOT FOUND for " + word + " !!!"


################################################

word_to_lookup = 'Katze'
word_to_lookup = 'Band'
word_to_lookup = 'Politikunterricht'
word_to_lookup = 'Nachteil'
word_to_lookup = 'Schuh'

if __name__ == '__main__':
    nounInflectionTableSearcher = NounInflectionTableSearcher()
    output = nounInflectionTableSearcher.get_noun_inflection_tables(word_to_lookup)
    print(output)
