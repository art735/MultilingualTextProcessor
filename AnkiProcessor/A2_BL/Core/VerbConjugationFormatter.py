import re

double_br_positive_lookbehind = r'(?<=(<br>){2})'
parameterized_positive_lookahead = r'(?={0})'

zeitformen_dict = {'Präsens': '\[ˈpʁɛːzɛns\]',
                   'Präteritum': '\[pʁɛˈteːʁitʊm\]',
                   'Partizip II': '\[paʁtiˈt͡siːp t͡svaɪ̯\]'}

bold_replacement = r'<b>{0}</b>'.format(r'\g<0>')


class VerbConjugationFormatter:
    def find_and_replace(self, html_str, search_regex, replacement):
        result = html_str

        replaced_str = re.sub(search_regex, replacement, html_str)  # replaces all occurrences

        if replaced_str != html_str:
            # if mode == Mode.SEARCH_ONLY:
            #     print("Verb conjugation formatting is needed:\n{0}\n".format(html_str))
            # elif mode == Mode.FIND_AND_REPLACE:
            result = replaced_str

        return result

    # Business method
    def format_verb(self, html_str):
        result = html_str

        for k, v in zeitformen_dict.items():
            if k in ['Präsens', 'Präteritum']:
                front_search_regex = '{0}{1}{2}'.format(double_br_positive_lookbehind, k,
                                                        parameterized_positive_lookahead.format(r'<br>ich'))

                transcription_search_regex = '{0}{1}{2}'.format(double_br_positive_lookbehind, v,
                                                                parameterized_positive_lookahead.format(r'<br>\[ɪç'))

                back_search_regex = double_br_positive_lookbehind + 'спряжение в {0}'.format(k)
                bold_and_partially_italic_replacement = r'<i>спряжение в <b>{0}</b></i>'.format(k)

            elif k in ['Partizip II']:
                front_search_regex = '{0}{1}{2}'.format(double_br_positive_lookbehind, k,
                                                        parameterized_positive_lookahead.format(r'<br>\w+?\Z'))

                # \w (lowercase w) matches a "word" character: a letter or digit or underbar [a-zA-Z0-9_].
                # Note that although "word" is the mnemonic for this, it only matches a single word char, not a whole word.

                transcription_search_regex = '{0}{1}{2}'.format(double_br_positive_lookbehind, v,
                                                                parameterized_positive_lookahead.format(
                                                                    r'<br>.+?\Z'))

                back_search_regex = double_br_positive_lookbehind + 'форма {0}\Z'.format(k)
                bold_and_partially_italic_replacement = r'<i>форма <b>{0}</b></i>'.format(k)

            result = self.find_and_replace(result, front_search_regex, bold_replacement)
            result = self.find_and_replace(result, transcription_search_regex, bold_replacement)
            result = self.find_and_replace(result, back_search_regex, bold_and_partially_italic_replacement)

        return result

##############################################################

# html_str = """geben<br><br>Präsens<br>ich gebe – wir geben<br>du gibst – ihr gebt<br>er/sie/es gibt – sie geben<br><br>Präteritum<br>ich gebe – wir geben<br>du gibst – ihr gebt<br>er/sie/es gibt – sie geben
#
# [ˈɡeːbn̩]<br><br>[ˈpʁɛːzɛns]<br>[ɪç ˈɡeːbə] – [viːɐ̯ ˈɡeːbn̩]<br>[duː ɡiːpst] – [iːɐ̯ ɡeːpt]<br>[eːɐ/ziː/ɛs̯ ɡiːpt] – [ziː ˈɡeːbn̩]<br><br>[pʁɛˈteːʁitʊm]<br>[ɪç ˈɡeːbə] – [viːɐ̯ ˈɡeːbn̩]<br>[duː ɡiːpst] – [iːɐ̯ ɡeːpt]<br>[eːɐ/ziː/ɛs̯ ɡiːpt] – [ziː ˈɡeːbn̩]
#
# давать<br><br>спряжение в Präsens<br><br>спряжение в Präteritum"""
#
# verbConjugationFormatter = VerbConjugationFormatter()
# res = verbConjugationFormatter.format(html_str, Mode.FIND_AND_REPLACE)
# print(res)
