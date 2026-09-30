import MethodExecutionTimeLogger
from GrammarEnums import ConversionMode
from N2_NounGrammarConverter import NounGrammarConverter

base_dir = r'E:\Languages\[Git repo] MultilingualTextProcessor\resources\Greek\\'


class GospelStatisticsProcessor:
    matthew_gospel_text = get_gospel_text('1Matthew.txt')
    mark_gospel_text = get_gospel_text('2Mark.txt')
    luke_gospel_text = get_gospel_text('3Luke.txt')
    john_gospel_text = get_gospel_text('4John.txt')

    # Данный список НЕ будет занимать память, равную сумме размеров всех входящих в него строк,
    # а только небольшую фиксированную память, необходимую для хранения четырёх ссылок на эти строки.
    all_four_gospels_list = [matthew_gospel_text, mark_gospel_text, luke_gospel_text, john_gospel_text]
    # all_four_gospels_text = " \n\n ".join(all_four_gospels_list)

    global_lemma_dict = {}

    nounGrammarConverter = NounGrammarConverter()

    def print_statistics(self):
        print(self.all_four_gospels_text)

    def _count_lemmas(self, gospel_author, gospel_text):
        local_lemma_dict = {}

        tuples = SpaCyEngineWrapper.get_doc_object_tuples(gospel_text)
        print(f'Number of tuples is {len(tuples)}')

        for token, lemma, pos, morph in tuples:
            # работа с глобальным "сквозным" для всех Евангелий словарём лемм
            if lemma not in self.global_lemma_dict:
                self.global_lemma_dict[lemma] = 1
                local_lemma_dict[lemma] = 1
            else:
                lemma_counter = self.global_lemma_dict[lemma]
                lemma_counter += 1
                self.global_lemma_dict[lemma] = lemma_counter

                if lemma in local_lemma_dict:
                    lemma_counter = local_lemma_dict[lemma]
                    lemma_counter += 1
                    local_lemma_dict[lemma] = lemma_counter
        # end of loop

        print("Gospel of {0}:".format(gospel_author.upper()))
        print("Unique lemmas in global_lemma_dict: " + str(len(self.global_lemma_dict.keys())))
        print("Unique lemmas in local_lemma_dict: " + str(len(local_lemma_dict.keys())))
        print("---------")

    def count_lemmas_of_four_gospels(self):

        self._count_lemmas('Matthew', self.matthew_gospel_text)
        # self._count_lemmas('Mark', self.mark_gospel_text)
        # self._count_lemmas('Luke', self.luke_gospel_text)
        # self._count_lemmas('John', self.john_gospel_text)

        # Сортировка словаря по убыванию значений
        # sorted_dict = dict(sorted(self.global_lemma_dict.items(), key=lambda item: item[1], reverse=True))

        ######### NEW CODE #######

        # Запись словаря в файл
        # Параметр ensure_ascii=False указывает json.dump(), что не нужно принудительно преобразовывать все не-ASCII
        # символы в Unicode-последовательности, что позволяет сохранить греческие символы в их нормальном виде.
        # with open(base_dir + r'1Matthew_freq_dict.json', 'w', encoding='utf-8') as json_file:
        #     json.dump(sorted_dict, json_file, ensure_ascii=False)

        # Запись частотного словаря в текстовый файл
        # with open(base_dir + r'5all_four_Gospels_freq_dict.txt', 'w', encoding='utf-8') as file:
        #     for key, value in sorted_dict.items():
        #         file.write(f'{key}:{value}\n')

    def gather_pos_statistics(self):

        pos_lemmas_dict = {}

        # Поскольку попытка передать на вход spaCy текст Четвероевангелия целиком (self.all_four_gospels_text)
        # приводит к ошибке выделения памяти под обработку такого огромного массива текста (требуется ок. 12 ГБ памяти),
        # будем передавать текст евангелий на вход spaCy по частям, по одному Евангелию за раз
        for gospel in self.all_four_gospels_list:
            # for gospel in [self.matthew_gospel_text[:100]]:

            tuples = SpaCyEngineWrapper.get_doc_object_tuples(gospel)

            for token, lemma, pos, morph in tuples:
                # если леммы ещё нет среди всех значений словаря.
                # Получается, что лемма, которая может выступать в тексте в виде разных частей речи, в данном случае
                # жёстко фиксируется под тем pos-тэгом, под которым она впервые встретилась и не обязательно, что это
                # будет самый частый случай её морфологического употребления
                if not self._is_lemma_among_dict_values(lemma, pos_lemmas_dict):
                    if pos not in pos_lemmas_dict:
                        pos_lemmas_dict[pos] = set()  # Создаём новое множество для лемм
                    # Метод .add() добавляет элемент в множество. Если элемент уже присутствует,
                    # он не будет добавлен снова (множество автоматически игнорирует дубликаты).
                    pos_lemmas_dict[pos].add(lemma)

        # объединяем частотность собственных и нарицательных существительных в одну категорию
        if 'NOUN' in pos_lemmas_dict and 'PROPN' in pos_lemmas_dict:
            # объединяем содержимое ключей и значений
            noun_propn_merged_key = 'NOUN + PROPN'
            noun_propn_merged_value = pos_lemmas_dict['NOUN'] | pos_lemmas_dict['PROPN']  # объединение множеств

            # удаляем разрозненные категории существительных
            del pos_lemmas_dict['NOUN']
            del pos_lemmas_dict['PROPN']

            # добавляем объединённую информацию в словарь
            pos_lemmas_dict[noun_propn_merged_key] = noun_propn_merged_value

        # Чтобы отсортировать словарь, в котором значения являются множествами (set), по количеству элементов
        # в этих множествах, вы можете использовать функцию sorted() в сочетании с функцией len()
        # для получения длины каждого множества.
        pos_lemmas_dict = dict(sorted(pos_lemmas_dict.items(), key=lambda item: len(item[1]), reverse=True))

        no_of_lemmas = sum([len(v) for k, v in pos_lemmas_dict.items()])
        print(f'Total number of lemmas: {no_of_lemmas}')

        for k, v in pos_lemmas_dict.items():
            # no_of_lemmas += len(v)
            # print(k + ":" + str(v))
            percentage = len(v) / no_of_lemmas * 100
            # print(k + " - " + str(len(v)))
            print(f'{k} - {len(v)} ({percentage:.2f}%)')

        # self._find_duplicate_lemmas(pos_lemmas_dict)

    def _is_lemma_among_dict_values(self, lemma, my_dict):
        for value_set in my_dict.values():
            if lemma in value_set:
                return True
        return False

    def gather_uniqueness_statistics(self):
        all_words_counter = 0
        unique_tokens_set = set()
        unique_lemmas_set = set()

        all_nouns_counter = 0
        unique_noun_tokens_set = set()
        unique_noun_lemmas_set = set()
        noun_tokens_morph_dict = {}

        all_verbs_counter = 0
        unique_verb_tokens_set = set()
        unique_verb_lemmas_set = set()
        verb_tokens_morph_dict = {}

        for gospel in self.all_four_gospels_list:
            # for gospel in [self.matthew_gospel_text[:50]]:

            tuples = SpaCyEngineWrapper.get_doc_object_tuples(gospel)

            # all_words_counter += len(tuples)

            for token, lemma, pos, morph in tuples:
                # Считаем количество всех слов в тексте
                all_words_counter += 1

                # Считаем количество уникальных слов в тексте
                unique_tokens_set.add(token)

                # Считаем количество уникальных лемм в тексте
                unique_lemmas_set.add(lemma)

                if pos in ['NOUN', 'PROPN']:
                    all_nouns_counter += 1
                    unique_noun_tokens_set.add(token)
                    unique_noun_lemmas_set.add(lemma)

                    # Строим частотный словарь морфологии по ключу: '{число} {падеж}'. Род существительного не важен
                    token_grammar = self._get_token_grammar(morph)
                    if token_grammar not in noun_tokens_morph_dict:
                        noun_tokens_morph_dict[token_grammar] = list()
                    noun_tokens_morph_dict[token_grammar].append(token)

                elif pos == 'VERB':
                    all_verbs_counter += 1
                    unique_verb_tokens_set.add(token)
                    unique_verb_lemmas_set.add(lemma)

                    # Строим частотный словарь морфологии по ключу morph
                    if morph not in verb_tokens_morph_dict:
                        verb_tokens_morph_dict[morph] = list()
                    verb_tokens_morph_dict[morph].append(token)

        print(f'Всех слов в тексте Четвероевангелия: {all_words_counter}')
        print(f'Уникальных слов в тексте Четвероевангелия: {len(unique_tokens_set)}')
        print(f'Уникальных лемм в тексте Четвероевангелия: {len(unique_lemmas_set)}\n')

        print(f'Всех существительных в тексте Четвероевангелия: {all_nouns_counter}')
        print(f'Уникальных существительных в тексте Четвероевангелия: {len(unique_noun_tokens_set)}')
        print(f'Уникальных лемм существительных в тексте Четвероевангелия: {len(unique_noun_lemmas_set)}\n')

        print(f'Всех глаголов в тексте Четвероевангелия: {all_verbs_counter}')
        print(f'Уникальных глаголов в тексте Четвероевангелия: {len(unique_verb_tokens_set)}')
        print(f'Уникальных лемм глаголов в тексте Четвероевангелия: {len(unique_verb_lemmas_set)}\n')

        # noun_tokens_morph_dict = dict(sorted(noun_tokens_morph_dict.items(), key=lambda item: len(item[1]), reverse=True))
        # verb_tokens_morph_dict = dict(sorted(verb_tokens_morph_dict.items(), key=lambda item: len(item[1]), reverse=True))

        # Морфологическая статистика по существительным
        self._print_freq_dict_with_80_percentage_delimiter(noun_tokens_morph_dict)

        print('')

        # Морфологическая статистика по глаголам
        self._print_freq_dict_with_80_percentage_delimiter(verb_tokens_morph_dict)

    def _get_token_grammar(self, morph):
        token_grammar = 'not defined'
        if str(morph):
            # gender_str = morph.get("Gender")[0]
            # gender = str_to_enum(GenderSpaCy, gender_str)
            #
            # number_str = morph.get("Number")[0]
            # number = str_to_enum(NumberSpaCy, number_str)
            #
            # case_str = morph.get("Case")[0]
            # case = str_to_enum(CaseSpaCy, case_str)

            token_grammar = self.nounGrammarConverter.convert(morph, ConversionMode.NUMBER_CASE)
        return token_grammar

    def _print_freq_dict_with_80_percentage_delimiter(self, morph_tokens_dict):

        sorted_morph_tokens_dict = dict(sorted(morph_tokens_dict.items(), key=lambda item: len(item[1]), reverse=True))
        total_tokens = sum([len(tokens) for morph, tokens in sorted_morph_tokens_dict.items()])

        cumulative_freq = 0
        percentage_threshold = 80
        should_print_80_percent_msg = True
        for morph, tokens in sorted_morph_tokens_dict.items():
            freq = len(tokens)
            # print(f'{morph}: {freq} --> {tokens}')
            print(f'{morph}: {freq}')
            cumulative_freq += freq
            cumulative_percentage = cumulative_freq / total_tokens * 100
            if cumulative_percentage >= percentage_threshold and should_print_80_percent_msg:
                print("---=== Достигнут 80%-й рубеж частот! ===---")
                should_print_80_percent_msg = False

    def count_max_word_length_of_token_and_lemma(self):

        token_max = ''
        lemma_max = ''

        token_max_length = 0
        lemma_max_length = 0

        tuples = SpaCyEngineWrapper.get_doc_object_tuples(self.all_four_gospels_text[:100])

        for token, lemma, pos, morph in tuples:
            if len(token) > token_max_length:
                token_max_length = len(token)
                token_max = token
            if len(lemma) > lemma_max_length:
                lemma_max_length = len(lemma)
                lemma_max = lemma

        print(f"Max token: {token_max}; its length is {token_max_length}")
        print(f"Max lemma: {lemma_max}; its length is {lemma_max_length}")

    def get_freq_dict(self):

        self._count_lemmas('Matthew', self.matthew_gospel_text)
        self._count_lemmas('Mark', self.mark_gospel_text)
        self._count_lemmas('Luke', self.luke_gospel_text)
        self._count_lemmas('John', self.john_gospel_text)

        # Сортировка словаря по убыванию значений
        sorted_dict = dict(sorted(self.global_lemma_dict.items(), key=lambda item: item[1], reverse=True))

        return sorted_dict


###############################################

gospelStatisticsProcessor = GospelStatisticsProcessor()
# MethodExecutionTimeLogger.run(gospelStatisticsProcessor.count_lemmas_of_four_gospels)
# print('#######################')
# MethodExecutionTimeLogger.run(gospelStatisticsProcessor.gather_pos_statistics)
MethodExecutionTimeLogger.run(gospelStatisticsProcessor.gather_uniqueness_statistics)

# MethodExecutionTimeLogger.run(gospelStatisticsProcessor.count_max_word_length_of_token_and_lemma)
# MethodExecutionTimeLogger.run(gospelStatisticsProcessor.count_max_word_length_of_token_and_lemma)
