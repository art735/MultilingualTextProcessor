import AppContext
import Utils
from A040_VocabFilesConsistencyChecker import A040_VocabFilesConsistencyChecker
from AnkiCardEntity import AnkiCardEntity
from CharConstants import SPACE_DASH_SPACE, PIPE
from DeuLemmaResolver import DeuLemmaResolver
from DeuDefiniteArticleService import DeuDefiniteArticleService
from ExcelService import ExcelService
from GermanNounDeclensionService import GermanNounDeclensionService
from OdtFilesService import OdtFilesService
from GermanPronounDeclensionService import GermanPronounDeclensionService
from GermanSentenceTranscriber import GermanSentenceTranscriber
from GermanVerbConjugationService import GermanVerbConjugationService
from GrammarEnums import ConversionMode
from N2_NounGrammarConverter import NounGrammarConverter
from N3_DashedArticledNounsComposer import DashedArticledNounsComposer
from OdtFileTableDao import OdtFileTableDao
from DeuSpaCyOrStanzaWrapper import DeuSpaCyOrStanzaWrapper
from SpaCyPosResolver import SpaCyPosResolver
from View_enums import CurrentLanguageComboBoxEnum


class A100_GermanTextMorphologicalAnalysisPerformer:

    def __init__(self):
        self.token = ''
        self.token_grammaticized = ''
        self.processed_lemma = ''
        self.pos = ''
        self.morph = ''

        self.deuSpaCyOrStanzaWrapper = DeuSpaCyOrStanzaWrapper()
        self.excelService = ExcelService()

        self.nounGrammarConverter = NounGrammarConverter()
        self.deuDefiniteArticleService = DeuDefiniteArticleService()
        self.dashedArticledNounsComposer = DashedArticledNounsComposer(DeuDefiniteArticleService())
        self.deuLemmaResolver = DeuLemmaResolver()

        # В модуле А10_NewLemmasFinder данный сервис переинциализируется каждый раз в обработчике. Читать там подробный
        #  комментарий.
        self.odtFilesService = None
        self.odtFileTableDao = OdtFileTableDao()
        self.germanPronounDeclensionService = GermanPronounDeclensionService()
        self.germanVerbConjugationService = GermanVerbConjugationService()
        self.spaCyPosResolver = SpaCyPosResolver()

        # key - token; value - pair/triplet of nouns with translation and grammar hint
        self.text_results_set = set()

        # TODO где должен инициализироваться: здесь или в обработчике?
        self.germanSentenceTranscriber = GermanSentenceTranscriber()
        # self.germanPopovTextTranscriber = GermanPopovTextTranscriber()
        self.germanNounDeclensionService = GermanNounDeclensionService()

    # Метод может работать в двух режимах:
    # 1) если параметр 'input_text' непустой, происходит обработка входного текста
    # 2) иначе, если параметр vocab_filename непустой, предложения (с их транскрипциями и переводами) вычитываются из
    # указанного Vocab-файла.
    def process_german_text(self, input_text='', vocab_filename_or_filenames=None):

        if not input_text and not vocab_filename_or_filenames:
            raise ValueError("Either 'input_text' or 'vocab_filename' should be specified!")
        elif input_text and vocab_filename_or_filenames:
            raise ValueError("'input_text' and 'vocab_filename' must NOT be specified at the same time!")

        self.odtFilesService = OdtFilesService()

        # Проверяем все ли слова текста присутствуют в вокабуляре (множестве [Vocab]-файлов).
        # Если нет - возвращаем список слов, которые нужно добавить в вокабуляр.
        # TODO Временно отключил валидацию
        # missing_words = self._validate_all_words_are_present_in_vocabulary(input_text)
        # if missing_words:
        #     output = '\n'.join(missing_words)
        #     return output

        # 1. Морф. формы всего текста для вставки их в Excel
        output_1_Excel_mf_results = []
        # 2. Информация для вставки в OO Writer
        output_2_OO_Writer_results = []

        if input_text:
            # Разбиваем текст на отдельные предложения (строки, библейские стихи)
            sentences = Utils.split_by(input_text, '\n')
            for self.sentence in sentences:
                excel_output, oo_Writer_output = self._process_sentence()
                output_1_Excel_mf_results.append(excel_output)
                output_2_OO_Writer_results.append(oo_Writer_output)
                # Добавляем в результаты и само предложение
                sentence_row_str = self._complete_sentence_with_transcription_and_translation()
                output_2_OO_Writer_results.append(sentence_row_str)
        elif vocab_filename_or_filenames:
            # Если входной параметр является строкой, то преобразуем его в список
            if isinstance(vocab_filename_or_filenames, str):
                vocab_filenames = [vocab_filename_or_filenames]
            elif isinstance(vocab_filename_or_filenames, list):
                vocab_filenames = vocab_filename_or_filenames

            for vocab_filename in vocab_filenames:
                sentences_entities = self.odtFileTableDao.convert_table_rows_to_anki_cards_of_single_file(
                    vocab_filename, read_words=False, read_sentences=True)
                for i, sentence_entity in enumerate(sentences_entities):
                    # if i <= 10:  # TODO: временная заглушка
                    # 'self.sentence' - это именно поле класса, а не просто локальная переменная, чтобы для отладочных
                    # целей к ней был доступ из методов _process_noun(), _process_verb() и т. д.
                    self.sentence = sentence_entity.front[-1]
                    excel_output, oo_Writer_output = self._process_sentence()
                    output_1_Excel_mf_results.append(excel_output)
                    output_2_OO_Writer_results.append(oo_Writer_output)
                    # Добавляем в результаты и само предложение
                    sentence_row_str = sentence_entity.to_str(format_type="front_transcription_back_with_comments")
                    output_2_OO_Writer_results.append(sentence_row_str)

        # Удаляем пустые строки из результирующих списков
        output_1_Excel_mf_results = [o1 for o1 in output_1_Excel_mf_results if o1]
        output_2_OO_Writer_results = [o2 for o2 in output_2_OO_Writer_results if o2]

        # 1. Вывод морф. форм всего текста для вставки их в Excel
        output_for_excel = 'MORPH FORMS TO ADD INTO EXCEL:\n'
        if output_1_Excel_mf_results:
            output_for_excel += '\n'.join(output_1_Excel_mf_results)
        else:
            output_for_excel += 'No new morph forms!'

        # 2. Вывод морф. форм всего текста для вставки их в OO Writer
        output_for_oo_writer = 'MORPH FORMS TO ADD INTO OO WRITER:\n'
        if output_2_OO_Writer_results:
            output_for_oo_writer += '\n'.join(output_2_OO_Writer_results)

        output = '\n\n'.join([output_for_excel, output_for_oo_writer])
        return output

    def _validate_all_words_are_present_in_vocabulary(self, input_text):
        # Ещё раз повторяем UC#4, т. к. валидируем консистентность всей коллекции слов в [Vocab]-файлах
        a040_VocabFilesConsistencyChecker = A040_VocabFilesConsistencyChecker()
        consistency_check_result = a040_VocabFilesConsistencyChecker.check_consistency()
        if consistency_check_result.lower() != 'ok':
            return consistency_check_result

        # Основная работа: проверяем наличие всех слов в [Vocab]-файлах
        results_dict = {}
        tuples = self.deuSpaCyOrStanzaWrapper.get_doc_object_tuples(input_text)
        for token, lemma, pos, morph in tuples:
            # Переиспользуем метод поиска лемм из модуля A10_NewLemmasFinder
            processed_lemma = self.deuLemmaResolver.get_single_lemma(token, lemma, pos, morph)

            is_absent_from_vocabulary = self.odtFilesService.is_word_absent_from_vocabulary(processed_lemma)
            is_absent_from_results_dict = processed_lemma not in results_dict

            if is_absent_from_vocabulary and is_absent_from_results_dict:
                results_dict[processed_lemma] = f'Word "{processed_lemma}" is absent from vocabulary! Please, add it!'

        return results_dict.values()

    def _process_sentence(self):

        # Три списка с результатами
        # 1. Морф. формы для вставки их в Excel
        sentence_excel_results = []
        # 2. Морф. формы, относящиеся к отдельному предложению и расположенные в отдельных от предложения строках
        # таблицы в OO Writer
        sentence_oo_writer_results1 = []
        # 3. Морф. формы только существительных, расположенные вместе с предложением в одной общей merged-строке
        # в OO Writer
        sentence_oo_writer_results2 = []

        tuples = self.deuSpaCyOrStanzaWrapper.get_doc_object_tuples(self.sentence)

        for self.token, self.lemma, self.pos, self.morph in tuples:
            excel_result = ''
            oo_writer_result = ''
            # если слово является собственным (proper) или нарицательным (common) существительным
            if self.spaCyPosResolver.is_noun(self.pos) and self.spaCyPosResolver.is_noun_in_non_initial_form(
                    self.morph):
                self.processed_lemma = self.deuLemmaResolver.get_single_lemma(self.token, self.lemma, self.pos,
                                                                               self.morph)
                excel_result, oo_writer_result = self._process_noun()
                # Непосредственно в одной ячейке с немецким предложением храним морфологию только существительных.
                # TODO отключил добавление морфологии существительных к предложению
                # sentence_oo_writer_results2.append(oo_writer_result)

            # spaCy не различает сильное, слабое и смешанное склонение прилагательных; здесь представлять интерес могут
            # степени сравнения прилагательных: Degree={Pos|Comp|Sup}
            # elif self.spaCyPosResolver.is_adjective(self.pos):

            # pos = 'AUX' - это модальные глаголы; pos = 'VERB' - это обычные глаголы
            elif self.spaCyPosResolver.is_aux_or_verb(self.pos) and self.spaCyPosResolver.is_verb_form_non_infinitive(
                    self.morph):
                self.processed_lemma = self.deuLemmaResolver.get_single_lemma(self.token, self.lemma, self.pos,
                                                                               self.morph)
                excel_result, oo_writer_result = self._process_verb()

                # print(f"pos = '{self.pos}'")
                # print(f"morph = '{self.morph}'")
                # print('**************')

            # местоимения и определители собраны в одном и том же Excel-листе 'Articles & Pronouns'
            # elif self.spaCyPosResolver.is_pronoun(self.morph) or self.spaCyPosResolver.is_determiner(self.pos):
            elif (self.spaCyPosResolver.is_personal_or_possessive_pronoun(self.morph) and
                  self.spaCyPosResolver.is_pronoun_in_non_initial_form(self.morph)):
                self.processed_lemma = self.deuLemmaResolver.get_single_lemma(self.token, self.lemma, self.pos,
                                                                               self.morph)
                # TODO: проверять на начальную форму
                excel_result, oo_writer_result = self._process_pronoun_and_determiner()
                # sentence_excel_results.append(excel_result)
                # sentence_oo_writer_results1.append(oo_writer_result)

                # print(f"pos = '{self.pos}'")
                # print(f"morph = '{self.morph}'")
                # print('**************')

            # код, идущий после проверок на соответствие частям речи
            sentence_excel_results.append(excel_result)
            sentence_oo_writer_results1.append(oo_writer_result)
        # end of loop

        # Преобразовываем списки с результатами в строковую форму, отбрасывая пустые строки
        excel_output = "\n".join([item for item in sentence_excel_results if item])
        oo_writer_output1 = "\n".join([item for item in sentence_oo_writer_results1 if item])

        # Делаем merge строк в пределах каждого столбца (в механике OO Writer) и объединяем их с помощью pipe
        # в одну широкую строку, содержащую морф. формы + предложение, к которому они относятся
        # col1_results = []
        # col2_results = []
        # col3_results = []
        # for line in sentence_oo_writer_results2:
        #     pieces = line.split("|")
        #     col1_results.append(pieces[0])
        #     col2_results.append(pieces[1])
        #     col3_results.append(pieces[2])
        #
        # # В первом столбце между иностранными словами должно быть в среднем на 1 newline больше, чтобы они стояли ровно
        # # напротив своих переводов, под каждым из которых подписан ещё и grammar_hint.
        # col1_results_output = (OO_WRITER_STRIPES_DELIMITER + '^^^').join(col1_results)
        # col2_results_output = (OO_WRITER_STRIPES_DELIMITER + '^^^').join(col2_results)
        # col3_results_output = OO_WRITER_STRIPES_DELIMITER.join(col3_results)
        # oo_writer_output2 = "|".join([col1_results_output, col2_results_output, col3_results_output])
        #
        # oo_writer_output = '\n'.join([oo_writer_output1, oo_writer_output2])

        # return excel_output, oo_writer_output1, oo_writer_output2
        # return excel_output, oo_writer_output
        return excel_output, oo_writer_output1

    # Дополняем предложение транскрипцией и переводом (здесь именно глагол complete в названии метода: так перевели
    # и Google Translate, и ChatGPT-4omni)
    def _complete_sentence_with_transcription_and_translation(self):
        # Первым делом, нужно попробовать найти предложение среди [Vocab]-файлов: оно там может присутствовать, если:
        # 1) на UI был выставлен флаг "Include sentences in output"
        # AND
        # 2) в предложении встретились новые слова
        # Это более предпочтительный вариант, т. к. предложение уже содержит транскрипцию и перевод.
        sentence_result = self.odtFilesService.find_sentence_in_vocabulary(self.sentence)
        # Если предложение среди [Vocab]-файлов найдено не было
        if not sentence_result:
            # Формируем транскрипцию предложения путём вычитки транскрипций всех его слов из "Deutsch Lexikon (!Popov).xls" и Wiktionary
            sentence_unknown_words, sentence_transcription = self.germanSentenceTranscriber.transcribe_sentence(
                self.sentence, True)
            # Перевод предложения неизвестен
            sentence_translation = '???'
            sentence_result = '|'.join([self.sentence, sentence_transcription, sentence_translation])

        return sentence_result

    def _process_noun(self):
        # В худшем случае в виде результатов вернём токен "как есть"
        # result1 = self.token
        # result2 = self.token
        result1 = ''
        result2 = ''

        # articled_token = self.nounDefiniteArticleService.add_definite_article_to_token(self.token, self.pos, self.morph)

        # if self.gender and self.number and self.case:
        # is_token_in_its_initial_dictionary_form = self.number == NumberSpaCy.Sing.value and self.case == CaseSpaCy.Nom.value
        # продолжаем обрабатывать токен только если он находится в отличном от начальной словарной формы состоянии
        # if self.is_token_not_in_its_initial_dictionary_form():

        # neut. sg. dat.
        token_grammar = self.nounGrammarConverter.convert(self.morph, ConversionMode.GENDER_NUMBER_CASE)
        # Если token_grammar не определён (технически пустая строка), то возвращаем пустые результаты. Возможно в другом
        # предложении это же слово будет иметь более удачную и полную с т. з. spaCy грамматику.
        if not token_grammar:
            return result1, result2
        # Одна и та же словоформа может представлять разные падежи!
        # Например, Ἰησοῦ - это и родительный, и звательный падеж!!!
        # Поэтому надо работать не просто с token, а с token_grammaticized и от него
        # тогда действительно можно требовать уникальности в 1-м столбце Excel-файла для морф. форм!
        # Ἰησοῦ (masc. sg. gen.)|ὁ Ἰησοῦς - τοῦ Ἰησοῦ|(nom. - gen.)
        # Ἰησοῦ (masc. sg. voc.)|ὁ Ἰησοῦς - Ἰησοῦ!|(nom. - voc.)

        # Büro (neut. sg. dat.)
        self.token_grammaticized = f'{self.token} ({token_grammar})'

        # морф. форма обрабатываемого слова НЕ должна находиться среди:
        # 1) Excel-списка уже изученных ранее морф. форм
        # 2) словаря-поля класса text_results_dict, содержащего уже обработанные токены всех предыдущих предложений текста
        is_token_grammaticized_absent_from_excel = not self.excelService.is_morph_form_present(
            self.token_grammaticized)
        is_token_grammaticized_absent_from_text_results_dict = self.token_grammaticized not in self.text_results_set

        if is_token_grammaticized_absent_from_excel and is_token_grammaticized_absent_from_text_results_dict:
            noun_declension_entity = self.germanNounDeclensionService.get_noun_declension_entity(self.processed_lemma)
            if not noun_declension_entity:
                result2 = f"No noun_declension_entity in Excel for '{self.processed_lemma}' in '{self.sentence}'"
                return result1, result2

            # Если существительное НЕ начинается с артикля (это касается большинства собственных существительных, но
            # распространяется также и на некоторые нарицательные существительные, например Deutsch - немецкий язык),
            # то такое существительное не представляет интереса как морфологическая форма: запись вида
            # 'Hamburg - Hamburg|(nom. - dat.)' или 'Deutsch - Deutsch|(nom. - acc.)' никакой полезной информации
            # с точки зрения изучения немецкого языка не добавляет. Поэтому игнорируем такие существительные.
            if self.deuDefiniteArticleService.not_starts_with_definite_article(self.processed_lemma):
                return result1, result2

            # TODO: Здесь именно self.lemma должна передаваться в метод, а не self.processed_lemma
            # das Büro – dem Büro|(nom. – dat.)
            dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(
                self.lemma, self.token, self.pos, self.morph, noun_declension_entity)
            # Если info_msg не пустое, значит процесс определения грамматики токена вышел за штатные рамки
            if info_msg:
                result2 = info_msg
                return result1, result2

            # Büro (neut. sg. dat.)|das Büro – dem Büro|(nom. – dat.)
            # result1 = self.token_grammaticized + "|" + dashed_nouns_with_piped_pars_grammar
            result1 = PIPE.join([self.token_grammaticized, dashed_nouns, grammar_hint])
            # sentence_results1.append(result1)
            self.text_results_set.add(self.token_grammaticized)

            # TODO: продолжаем работу для формирования результата по 2-й категории
            transcriptions = []
            split_dashed_nouns = dashed_nouns.split(SPACE_DASH_SPACE)
            for articled_noun_form in split_dashed_nouns:
                noun_form_transcription = noun_declension_entity.find_transcription(articled_noun_form)
                transcriptions.append(noun_form_transcription)
            transcription = SPACE_DASH_SPACE.join(transcriptions)

            front = dashed_nouns
            if len(split_dashed_nouns) == 2:
                # 'die Straße – der Straße' - это '(nom. – gen.)' или '(nom. – dat.)'? Front-поле в Anki должно быть
                # уникальным и без доп. хинта в поле Front различить эти два случая не получится. Такая неопределённая
                # ситуация возникает только для сущ. ж.р. в gen. и dat.
                if split_dashed_nouns[0].startswith('die') and split_dashed_nouns[1].startswith('der'):
                    front = "{0}^^^{1}".format(dashed_nouns, grammar_hint)

            result2 = self._compose_result2(front, transcription, grammar_hint)

        return result1, result2

    def _process_pronoun_and_determiner(self):
        # В худшем случае в виде результатов вернём токен "как есть"
        # result1 = self.token
        # result2 = self.token
        result1 = ''
        result2 = ''

        is_token_absent_from_excel = not self.excelService.is_morph_form_present(self.processed_lemma)
        is_token_absent_from_text_results_dict = self.processed_lemma not in self.text_results_set

        if is_token_absent_from_excel and is_token_absent_from_text_results_dict:
            result1 = self.processed_lemma
            self.text_results_set.add(result1)

            front, transcription = self.germanPronounDeclensionService.get_pronoun_declension(self.processed_lemma)
            grammar_hint = '(declension)'

            result2 = self._compose_result2(front, transcription, grammar_hint)

        return result1, result2

    def _process_verb(self):

        result1 = ''
        result2 = ''

        infinitive = self.processed_lemma

        grammar_hint = self.germanVerbConjugationService.get_grammar_hint(self.morph)
        token_grammaticized = f'{infinitive} {grammar_hint}'

        # Дублирующийся код с process_noun, подумать как избежать дубликации кода
        is_morph_form_absent_from_excel = not self.excelService.is_morph_form_present(
            token_grammaticized)
        is_morph_form_absent_from_text_results_dict = token_grammaticized not in self.text_results_set

        if is_morph_form_absent_from_excel and is_morph_form_absent_from_text_results_dict:
            conjugation = self.germanVerbConjugationService.get_verb_conjugation(infinitive, self.morph)
            # Если conjugation не содержит символа PIPE, значит, скорей всего, spaCy ошибся с pos-тэгированием слов в
            # предложении и посчитал глаголом такое слово, которое глаголом на самом деле не является.
            # Например, в предложении 'Schönen Urlaub!' spaCy считает слово 'Schönen' глаголом.
            if PIPE not in conjugation:
                return result1, result2

            self.text_results_set.add(token_grammaticized)
            result1 = token_grammaticized

            front, transcription = conjugation.split('|')
            result2 = self._compose_result2(front, transcription, grammar_hint)

        return result1, result2

    def _compose_result2(self, front, transcription, grammar_hint):
        front_comment = []
        back = []
        back_comment = []

        # Вычитываем word_entity из .odt-файла
        word_entity = self.odtFilesService.get_word_entity(self.processed_lemma)
        if word_entity:
            # Заполняем поле front_comment
            front_comment = word_entity.front_comment

            # Заполняем поле back
            translation = word_entity.back[-1]
            back = ["{0}^^^{1}".format(translation, grammar_hint)]  # строка, обёрнутая в список

            # Заполняем поле back_comment
            back_comment = word_entity.back_comment

        result2_card = AnkiCardEntity(front=front, front_comment=front_comment, transcription=transcription,
                                      back=back, back_comment=back_comment)

        # result2 = '|'.join([front, front_comment, transcription, back, back_comment])
        result2 = result2_card.to_str("front_transcription_back_with_comments")
        return result2


##########################################################################################

text = """
Ab morgen muss ich arbeiten.
Ich bin oft im Büro, aber nur für wenige Stunden.
Wir fahren um zwölf Uhr ab.
"""

text = """
Ab morgen muss ich arbeiten.
Ich bin oft im Büro, aber nur für wenige Stunden.
Wir fahren um zwölf Uhr ab.
"""

# text = """
# Ich arbeite.
# Ich arbeitete.
# Ich werde arbeiten.
# """
#
# text = """
# Ich habe gearbeitet.
# Ich hatte gearbeitet.
# Ich werde gearbeitet haben.
# """

# text = """
# Der arbeitende Mann ist fleißig.
# Ich habe gestern viel gearbeitet.
# """

# text = 'Ich habe gearbeitet.'
# text = 'gearbeitet.'

# text = 'Er sagt, er gehe heute ins Kino.'
# text = 'Wenn ich reich wäre, würde ich um die Welt reisen.'

# text = 'Neue Bücher liegen auf dem Tisch.'
# text = 'Gib mir Kraft!'
# text = 'Schreibe einen Brief!'

# text = 'Ich bin oft im Büro, aber nur für wenige Stunden.'
# text = 'Ich habe die Katze.'

text = """
Ich bin oft im Büro, aber nur für wenige Stunden.
Wir fahren um zwölf Uhr ab.
"""

text = """
Fahren Sie an der nächsten Straße nach rechts.
Sie wohnt am Anfang der Straße.
"""

text = 'Wir sind im Moment nicht da.'
text = 'Sie wohnt am Anfang der Straße.'
text = 'Sie wohnt in Hamburg.'
text = 'Sie wohnt in der Ukraine.'

# text = """
# Fahren Sie an der nächsten Straße nach rechts.
# Die Kinder spielen auf der Straße.
# """

text = """
Fahren Sie an der nächsten Straße nach rechts.
Fahren Sie an der nächsten Straße nach rechts.
"""

if __name__ == '__main__':
    language = CurrentLanguageComboBoxEnum.GERMAN.value
    # language = CurrentLanguageComboBoxEnum.MODERN_GREEK.value
    # language = CurrentLanguageComboBoxEnum.ANCIENT_GREEK.value
    AppContext.switch_language(language)
    base_dir = AppContext.get_base_dir()

    a100_GermanTextMorphologicalAnalysisPerformer = A100_GermanTextMorphologicalAnalysisPerformer()

    # Вызов метода с заданным параметром 'input_text'
    # res = a100_GermanTextMorphologicalAnalysisPerformer.process_german_text(input_text=text)

    # Вызов метода с заданным параметром 'vocab_filename'
    # TODO: запускать повторно и убедиться, что никаких новых флексий не появляется; вывод должен содержать только предложения
    # vocab_filenames = FilenameUtils.get_all_vocab_filenames()

    vocab_filenames = [
        fr'{base_dir}\A1\Aa\[!Vocab] Aa.odt',
        # fr'{base_dir}\A1\Bb\[!Vocab] Bb.odt',
        # fr'{base_dir}\A1\Cc-Dd\[!Vocab] Cc-Dd.odt',
        # fr'{base_dir}\A1\Ee\[!Vocab] Ee.odt',
        # fr'{base_dir}\A1\Ff\[!Vocab] Ff.odt',
        # fr'{base_dir}\A1\Gg\[!Vocab] Gg.odt',
        # fr'{base_dir}\A1\Hh-Jj\[!Vocab] Hh-Jj.odt',
        # fr'{base_dir}\A1\Kk\[!Vocab] Kk.odt',
        # fr'{base_dir}\A1\Ll-Mm\[!Vocab] Ll-Mm.odt',
        # fr'{base_dir}\A1\Nn-Rr\[!Vocab] Nn-Rr.odt',
        # fr'{base_dir}\A1\Ss\[!Vocab] Ss.odt',
        # fr'{base_dir}\A1\Tt-Vv\[!Vocab] Tt-Vv.odt',
        # fr'{base_dir}\A1\Ww-Zz\[!Vocab] Ww-Zz.odt'
    ]

    res = a100_GermanTextMorphologicalAnalysisPerformer.process_german_text(vocab_filename_or_filenames=vocab_filenames)

    print(res)
