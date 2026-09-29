import re



class TranscriptionFinal_ɪ_with_i_SoundReplacer:

    # Список гласных для того, чтобы убедиться, что после них стоит звук 'ɪ' (а не 'i'). Но из этого правила тоже
    # есть исключения: например, женское имя Chloe ['kl̲oʊ.i] содержит звук 'i' после гласного (дифтонг 'oʊ').
    # В этом случае хорошо помогает точка, разделяющая дифтонг и гласную 'i'. Благодаря этой точке такая транскрипция
    # захватываться не будет, а значит останется немодифицированной в своём правильном виде.
    eng_ipa_vowels = ["i", "ɪ", "e", "ɛ", "æ", "ə", "ʌ", "ɑ", "a", "ɒ", "ɔ", "ʊ", "u"]
    eng_ipa_vowels_pattern = f'[{"".join(eng_ipa_vowels)}]'

    def __init__(self):
        pass

    def replace_final_ɪ_with_i(self, bracketed_transcription):
        # заменить на 'i' такой звук 'ɪ', за которым positive lookahead может обнаружить необязательную ']', но дальше
        # в любом случае должен следовать пробел или конец строки
        # updated_transcription = re.sub(r'ɪ(?=\]?(\s|$))', 'i', bracketed_transcription)

        # Произвести замену 'ɪ' -> 'i' если:
        # - перед 'ɪ' находится не-гласный звук (т. е. фактически согласный звук, но с согласными сложнее работать из-за
        # того, что они могут быть альвеолярными/ассимилированными т. д., поэтому формулируем правило через ГЛАСНЫЕ
        # звуки)
        # - за 'ɪ' следует пробел или закрывающая квадратная скобка
        # negative lookbehind + ɪ + positive lookahead
        updated_transcription = re.sub(
            fr'(?<!{self.eng_ipa_vowels_pattern})ɪ(?=[\s\]])', 'i', bracketed_transcription)
        return updated_transcription


###################################################

transcription = "пример слова с ɪ и в скобках [ɪ]"
transcription = "['sɪtɪ 'lɪlɪ]"
transcription = "['s̲pes̲ɪfaɪ]"

if __name__ == '__main__':
    transcriptionFinal_ɪ_with_i_SoundReplacer = TranscriptionFinal_ɪ_with_i_SoundReplacer()
    res = transcriptionFinal_ɪ_with_i_SoundReplacer.replace_final_ɪ_with_i(transcription)
    print(res)

    input1 = [
        "пример слова с ɪ и в скобках [ɪ]", "['sɪtɪ 'lɪlɪ]",
        # Негативные сценарии (перед 'ɪ' стоит гласный, поэтому замена не должна производиться)
        "['s̲pes̲ɪfaɪ]"
    ]

    er1 = [
        "пример слова с i и в скобках [i]", "['sɪti 'lɪli]",
        # Негативные сценарии (перед 'ɪ' стоит гласный, поэтому замена не должна производиться)
        "['s̲pes̲ɪfaɪ]",
    ]

    if all(transcriptionFinal_ɪ_with_i_SoundReplacer.replace_final_ɪ_with_i(input_val) == er for input_val, er in
           zip(input1, er1)):
        print('test1 ok')
    else:
        print('test1 failed')
