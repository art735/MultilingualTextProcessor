import re

# Количество часов может передаваться одной (9.xy Uhr) или двумя (16.xy Uhr) цифрами.
hours = r'0?\d{1,2}'
# Считаем, что количество минут ВСЕГДА передаётся 2-мя цифрами при использовании формата ab.xy Uhr
minutes = r'\d{2}'
hours_minutes_pattern = fr'{hours}\.{minutes}'
hours_minutes_pattern_with_possible_uhr = fr'{hours_minutes_pattern}(?:\sUhr)?'

HOURS_MINUTES_SEPARATOR = '.'


# Правило чтения фразы 'von X bis Y Uhr':
# 1. В первой части выражения (после “von”) слово “Uhr” произносится если указаны минуты и их кол-во отлично от нуля.
# 2. В конце выражения (после “bis”) слово “Uhr” произносится всегда, независимо от наличия минут.
# Полный разбор правила и сравнение ответов от разных AI-чатов читать в следующем файле:
# \resources\German\Goethe-Institut A1, A2, B1 docs\A1\Правила чтения фразы 'von X bis Y Uhr'.odt
class GermanTimeTranscribableMaker:
    def __init__(self):
        pass

    def make_time_transcribable(self, sentence):
        if 'Uhr' not in sentence:
            return sentence

        von_bis_pattern = fr'[Vv]on {hours_minutes_pattern} bis {hours_minutes_pattern_with_possible_uhr}'

        # Начинаем поиск фраз, содержащих время от более конкретного (длинного) шаблона до более общего и короткого
        match = re.search(von_bis_pattern, sentence)
        if match:
            # Всю захваченную фразу разбиваем на отдельные слова
            pieces = match.group(0).split()
            first_timestamp = pieces[1]  # напр., 12.00
            second_timestamp = pieces[3]  # напр., 12.30

            first_timestamp_processed = self._process_timestamp(first_timestamp, should_add_uhr=False)
            second_timestamp_processed = self._process_timestamp(second_timestamp, should_add_uhr=True)

            # Заменяем время в исходном тексте
            pieces[1] = first_timestamp_processed
            pieces[3] = second_timestamp_processed

            # Удаляем слово 'Uhr' в конце фразы (если оно есть)
            if pieces[-1] == 'Uhr':
                del pieces[-1]

            # Восстанавливаем захваченную фразу с подменёнными значениями времени
            restored_phrase = ' '.join(pieces)
            # Заменяем захваченную фразу в исходном тексте на её обновлённый вариант
            sentence = sentence.replace(match.group(0), restored_phrase)
        else:
            match = re.search(hours_minutes_pattern_with_possible_uhr, sentence)
            if match:
                pieces = match.group(0).split()
                timestamp = pieces[0]
                timestamp_processed = self._process_timestamp(timestamp, should_add_uhr=True)
                sentence = sentence.replace(match.group(0), timestamp_processed)

        return sentence

    # Флаг should_add_uhr регулирует добавление слова 'Uhr' к временной метке.
    # Общее правило указано в описании к данному классу и дублируется здесь:
    # Правило чтения фразы 'von X bis Y Uhr':
    # 1. В первой части выражения (после “von”) слово “Uhr” произносим, если указаны минуты и их кол-во отлично от нуля.
    # 2. В конце выражения (после “bis”) слово “Uhr” произносится всегда, независимо от наличия минут.
    def _process_timestamp(self, timestamp, should_add_uhr):
        hours, minutes = timestamp.split(HOURS_MINUTES_SEPARATOR)

        # Если кол-во часов или минут начинается с '0', убираем этот ноль
        if hours.startswith('0'):
            hours = hours[1:]
        if minutes.startswith('0'):
            minutes = minutes[1:]

        if minutes == '0':  # если количество минут равно '00' (один ведущий ноль уже убрали раньше)
            if should_add_uhr:
                result = f'{hours} Uhr'
            else:
                result = f'{hours}'
        else:
            result = f'{hours} Uhr {minutes}'

        # print(result)
        return result


###############################################

sentence = 'Der Laden ist samstags bis 09.00 Uhr geöffnet.'
sentence = 'Von 12.00 bis 12.30 Uhr haben wir Mittagspause.'

if __name__ == '__main__':
    germanTimeTranscribableMaker = GermanTimeTranscribableMaker()
    # res = germanTimeTranscribableMaker.make_transcribable(sentence)
    # print(res)

    # TC #1
    input1 = [
        # Кол-во часов начинается с '0' (занимает один разряд)
        'Der Laden ist samstags bis 09.00 Uhr geöffnet.',
        'Der Laden ist samstags bis 09.08 Uhr geöffnet.',
        'Der Laden ist samstags bis 09.20 Uhr geöffnet.',

        # Кол-во часов занимает все 2 разряда
        'Der Laden ist samstags bis 19.00 Uhr geöffnet.',
        'Der Laden ist samstags bis 19.08 Uhr geöffnet.',
        'Der Laden ist samstags bis 19.20 Uhr geöffnet.',

        # Предложния с фразой von...bis...
        'Von 12.00 bis 13.00 Uhr haben wir Mittagspause.',
        'Von 12.00 bis 12.30 Uhr haben wir Mittagspause.',
        'Von 12.30 bis 13.00 Uhr haben wir Mittagspause.',
        'Von 12.30 bis 13.30 Uhr haben wir Mittagspause.',

        # Фраза von...bis... без указания минут в виде 00 после точки
        'Von 12 bis 13 Uhr haben wir Mittagspause.',
        'Von 12 bis 12.30 Uhr haben wir Mittagspause.',
        'Von 12.30 bis 13 Uhr haben wir Mittagspause.',
        'Von 12.30 bis 13.30 Uhr haben wir Mittagspause.',
    ]

    er1 = [
        'Der Laden ist samstags bis 9 Uhr geöffnet.',
        'Der Laden ist samstags bis 9 Uhr 8 geöffnet.',
        'Der Laden ist samstags bis 9 Uhr 20 geöffnet.',

        'Der Laden ist samstags bis 19 Uhr geöffnet.',
        'Der Laden ist samstags bis 19 Uhr 8 geöffnet.',
        'Der Laden ist samstags bis 19 Uhr 20 geöffnet.',

        'Von 12 bis 13 Uhr haben wir Mittagspause.',
        'Von 12 bis 12 Uhr 30 haben wir Mittagspause.',
        'Von 12 Uhr 30 bis 13 Uhr haben wir Mittagspause.',
        'Von 12 Uhr 30 bis 13 Uhr 30 haben wir Mittagspause.',

        'Von 12 bis 13 Uhr haben wir Mittagspause.',
        'Von 12 bis 12 Uhr 30 haben wir Mittagspause.',
        'Von 12 Uhr 30 bis 13 Uhr haben wir Mittagspause.',
        'Von 12 Uhr 30 bis 13 Uhr 30 haben wir Mittagspause.',
    ]

    if all(germanTimeTranscribableMaker.make_time_transcribable(input_val) == er for input_val, er in zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
