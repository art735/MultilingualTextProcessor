from LargeTextIntoChunksForNlpSplitter import LargeTextIntoChunksForNlpSplitter


class BaseSpaCyOrStanzaWrapper:
    def __init__(self, nlp_engine, lang_model, textPreprocessor):
        # Формируем nlp-объект, загружая в spaCy или Stanza (через spaCy-обёртку) языковую модель
        if nlp_engine == 'spaCy':
            import spacy
            self.nlp = spacy.load(lang_model)
        elif nlp_engine == 'Stanza':
            import spacy_stanza
            # Загружаем модель Stanza через spaCy-обёртку для сохранения единого spaCy-интерфейса в дальнейшей работе
            # с doc-объектом
            # В Stanza процессор `pos` отвечает и за определение частей речи, и за морфологические признаки (feats).
            # Отдельного процессора `morph` в списке `processors` указывать не нужно (он входит в состав `pos`).
            # `tokenize`: Разбивает текст на предложения и токены.
            # `mwt`: (Multi-Word Token) Критически важен для греческого языка (например, для разделения слитных артиклей и предлогов).
            # `pos`: Определяет части речи (UPOS, XPOS) и морфологические признаки (UFeats).
            self.nlp = spacy_stanza.load_pipeline(
                name=lang_model,  # код языка для spaCy (например: "en", "de", "el")
                lang=lang_model,  # код языка для Stanza; определяет, какую языковую модель загрузить
                processors="tokenize,mwt,pos,lemma",
                use_gpu=False
            )
        else:
            raise ValueError(f"Engine '{nlp_engine}' is not supported!")

        self.textPreprocessor = textPreprocessor
        self.largeTextIntoChunksForNlpSplitter = LargeTextIntoChunksForNlpSplitter()

    def process(self, input_text, should_split_large_text_into_chunks=False):
        # 1. Осуществляем препроцессинг входного текста
        preprocessed_text = self.textPreprocessor.preprocess(input_text)

        # 2. Разбиваем потенциально большой входной текст на чанки и формируем для них список doc-объектов
        doc_objects = []
        if should_split_large_text_into_chunks:
            text_chunks = self.largeTextIntoChunksForNlpSplitter.split_large_text(preprocessed_text)
            for text_chunk in text_chunks:
                doc = self.nlp(text_chunk)
                # TODO если памяти на хранение списка doc-объектов хватать не будет, придётся уже здесь формировать
                #  список кортежей (token, lemma, pos, morph, etc.)
                doc_objects.append(doc)
        else:
            doc = self.nlp(preprocessed_text)
            doc_objects.append(doc)

        return doc_objects
