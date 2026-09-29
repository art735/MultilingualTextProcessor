# Структура текстового файла:
# # Эпизод 1
# [Текст субтитров эпизода 1]
#
# # Эпизод 2
# [Текст субтитров эпизода 2]
#
# ...
#
# # Эпизод 76
# [Текст субтитров эпизода 76]
import FileContentsReader


class NicosWegSubtitlesProcessor:

    def get_episode_subtitles(self, text, episode_number):
        # {episode_number:02} означает использование формата 02 для отображения номера эпизода с ведущими нулями,
        # например, 01, 02, 03 и т. д.
        start_marker = f"[Folge {episode_number:02}]"
        next_marker = f"[Folge {episode_number + 1:02}]"

        # Найти начало и конец эпизода
        start_idx = text.find(start_marker)
        if start_idx == -1:
            return f"Эпизод {episode_number} не найден."

        start_idx += len(start_marker)
        end_idx = text.find(next_marker, start_idx)

        if end_idx == -1:
            return text[start_idx:].strip()  # Если это последний эпизод

        return text[start_idx:end_idx].strip()


#########################################################

if __name__ == '__main__':
    nicosWegSubtitlesProcessor = NicosWegSubtitlesProcessor()

    # Пример использования
    filename = r'/Nicos Weg (A1) subtitles-de.txt'
    # all_subtitles = nicosWegSubtitlesProcessor.load_subtitles(filename)
    all_subtitles = FileContentsReader.get_file_text(filename)
    episode_number = 76  # Номер эпизода, который хотите вычитать
    episode_subtitles = nicosWegSubtitlesProcessor.get_episode_subtitles(all_subtitles, episode_number)

    print(episode_subtitles)
