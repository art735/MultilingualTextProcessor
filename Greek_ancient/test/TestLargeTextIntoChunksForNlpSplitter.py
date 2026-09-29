from unittest import TestCase

from LargeTextIntoChunksForNlpSplitter import LargeTextIntoChunksForNlpSplitter

text = """
Ab morgen muss ich arbeiten.
Ich bin oft im Büro, aber nur für wenige Stunden.
Wir fahren um zwölf Uhr ab.
"""


class TestLargeTextIntoChunksForNlpSplitter(TestCase):

    def setUp(self):
        self.largeTextIntoChunksForNlpSplitter = LargeTextIntoChunksForNlpSplitter()

    def test_split_large_text_into_chunks_by_newline(self):
        # Во внешнем цикле определяем размер чанка
        for chunk_size in range(0, len(text) + int(len(text) / 2)):
            chunks = self.largeTextIntoChunksForNlpSplitter.split_large_text(text, chunk_size=chunk_size)
            # размер всех чанков (кроме последнего) должен быть >= заданного размера чанка
            # размер последнего чанка - ненулевой
            for i in range(0, len(chunks) - 1):
                self.assertGreaterEqual(len(chunks[i]), chunk_size, "Длина чанка должна быть не менее chunk_size")
            self.assertGreaterEqual(len(chunks[-1]), 1, "Длина последнего чанка должна быть ненулевой")

            # Восстановленный из чанков текст должен быть равен исходному тексту
            restored_text = ''.join(chunks)
            self.assertEqual(text, restored_text)
