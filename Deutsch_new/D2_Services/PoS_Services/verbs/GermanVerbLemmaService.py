import re

import GermanPronounHelper
from CharConstants import SPACE_DASH_SPACE
from FrontAndTranscriptionEntity import FrontAndTranscriptionEntity
from GermanVerbConjugationDao import GermanVerbConjugationDao


class GermanVerbLemmaService:

    def __init__(self):
        self.germanVerbConjugationDao = GermanVerbConjugationDao()
        self.verb_entities = self.germanVerbConjugationDao.convert_excel_rows_to_entities()

    def find_verb_lemma(self, verb_form):
        result = ''
        verb_form = verb_form.lower()

        for verb_entity in self.verb_entities:
            if verb_entity.infinitive == verb_form:
                result = verb_entity.infinitive
            else:
                # Перебор всех полей сущности GermanVerbConjugationEntity и проверка на тип FrontAndTranscriptionEntity.
                # vars(verb_entity) возвращает словарь всех атрибутов экземпляра verb_entity
                for attr_name, attr_value in vars(verb_entity).items():
                    if isinstance(attr_value, FrontAndTranscriptionEntity):
                        # print(f"Поле '{attr_name}' имеет тип FrontAndTranscriptionEntity.")
                        # Здесь можно заглянуть внутрь объекта
                        # print(f"Front: {attr_value.front}, Transcription: {attr_value.transcription}")
                        for front_item in attr_value.front:
                            if self._check_whether_verb_form_matches(verb_form, front_item):
                                result = verb_entity.infinitive
                                break

        # if result == '':
        #     result = 'No verb with such form in Deutsch Lexikon (!Popov).xls'

        return result

    def _check_whether_verb_form_matches(self, verb_form, front_item):
        result = False
        # Разбиваем front_item вида 'ich bin – wir sind' на части
        front_item_pieces = front_item.split(SPACE_DASH_SPACE)
        for front_item_piece in front_item_pieces:
            pure_verb_form = GermanPronounHelper.strip_personal_pronoun_before_verb(front_item_piece)

            # актуально для форм императива: приводим pure_verb_form к нижнему регистру и удаляем восклицательный знак
            # в конце, а также в целом для всех форм делаем strip() на всякий случай
            pure_verb_form = pure_verb_form.lower().replace('!', '').strip()

            if re.match(f'^{verb_form}$', pure_verb_form):
                result = True
                break

        return result


##################################

verb_form = 'willst'
verb_form = 'bin'
verb_form = 'rauchten'
verb_form = 'Schreibe'
verb_form = 'geben'
verb_form = 'mach'
verb_form = 'zieh'
verb_form = 'sprichst'

if __name__ == '__main__':
    germanVerbLemmaService = GermanVerbLemmaService()
    res = germanVerbLemmaService.find_verb_lemma(verb_form)
    print(res)
