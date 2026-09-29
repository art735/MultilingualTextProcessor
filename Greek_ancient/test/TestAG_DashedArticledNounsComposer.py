from unittest import TestCase

from GrcDefiniteArticleService import GrcDefiniteArticleService
from N3_DashedArticledNounsComposer import DashedArticledNounsComposer


class TestAG_DashedArticledNounsComposer(TestCase):
    sg_nom_msg = "Word '{0}' is in its initial dictionary form (sg. nom.)"
    piped_pair = "{0}|{1}"

    def setUp(self):
        self.dashedArticledNounsComposer = DashedArticledNounsComposer(GrcDefiniteArticleService())
        self.pos = 'NOUN'

    def get_actual_result(self, dashed_nouns, grammar_hint, info_msg):
        if info_msg:
            actual_result = info_msg
        else:
            actual_result = self.piped_pair.format(dashed_nouns, grammar_hint)
        return actual_result

    def test_masc(self):
        lemma = 'ἄνθρωπος'

        # SINGULAR NUMBER
        # nominative sg.
        token = "ἄνθρωπος"
        expected_result = self.sg_nom_msg.format(token)
        morph = {'Case': ['Nom'], 'Gender': ['Masc'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive sg.
        token = "ἀνθρώπου"
        expected_result = 'ὁ ἄνθρωπος – τοῦ ἀνθρώπου|(nom. – gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Masc'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative sg.
        token = "ἀνθρώπῳ"
        expected_result = 'ὁ ἄνθρωπος – τῷ ἀνθρώπῳ|(nom. – dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Masc'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative sg.
        token = "ἄνθρωπον"
        expected_result = 'ὁ ἄνθρωπος – τόν ἄνθρωπον|(nom. – acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Masc'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative sg.
        token = "ἄνθρωπε"
        expected_result = 'ὁ ἄνθρωπος – ἄνθρωπε!|(nom. – voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Masc'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # DUAL NUMBER
        # nominative du.
        token = "ἀνθρώπω"
        expected_result = 'ὁ ἄνθρωπος – τὼ ἀνθρώπω|(sg. – du.)'
        morph = {'Case': ['Nom'], 'Gender': ['Masc'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive du.
        token = "ἀνθρώποιν"
        expected_result = 'ὁ ἄνθρωπος – τὼ ??? – τοῖν ἀνθρώποιν|(sg. – du. nom. – du. gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Masc'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative du.
        token = "ἀνθρώποιν"
        expected_result = 'ὁ ἄνθρωπος – τὼ ??? – τοῖν ἀνθρώποιν|(sg. – du. nom. – du. dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Masc'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative du.
        token = "ἀνθρώπω"
        expected_result = 'ὁ ἄνθρωπος – τὼ ??? – τὼ ἀνθρώπω|(sg. – du. nom. – du. acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Masc'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative du.
        token = "ἀνθρώπω"
        expected_result = 'ὁ ἄνθρωπος – τὼ ??? – ἀνθρώπω!|(sg. – du. nom. – du. voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Masc'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # PLURAL NUMBER
        # nominative pl.
        token = "ἄνθρωποι"
        expected_result = 'ὁ ἄνθρωπος – οἱ ἄνθρωποι|(sg. – pl.)'
        morph = {'Case': ['Nom'], 'Gender': ['Masc'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive pl.
        token = "ἀνθρώπων"
        expected_result = 'ὁ ἄνθρωπος – οἱ ??? – τῶν ἀνθρώπων|(sg. – pl. nom. – pl. gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Masc'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative pl.
        token = "ἀνθρώποις"
        expected_result = 'ὁ ἄνθρωπος – οἱ ??? – τοῖς ἀνθρώποις|(sg. – pl. nom. – pl. dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Masc'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative pl.
        token = "ἀνθρώπους"
        expected_result = 'ὁ ἄνθρωπος – οἱ ??? – τοὺς ἀνθρώπους|(sg. – pl. nom. – pl. acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Masc'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative pl.
        token = "ἄνθρωποι"
        expected_result = 'ὁ ἄνθρωπος – οἱ ??? – ἄνθρωποι!|(sg. – pl. nom. – pl. voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Masc'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

    def test_fem(self):
        lemma = 'γυνή'

        # SINGULAR NUMBER
        # nominative sg.
        token = "γυνή"
        expected_result = self.sg_nom_msg.format(token)
        morph = {'Case': ['Nom'], 'Gender': ['Fem'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive sg.
        token = "γυναικός"
        expected_result = 'ἡ γυνή – τῆς γυναικός|(nom. – gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Fem'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative sg.
        token = "γυναικί"
        expected_result = 'ἡ γυνή – τῇ γυναικί|(nom. – dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Fem'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative sg.
        token = "γυναῖκα"
        expected_result = 'ἡ γυνή – τὴν γυναῖκα|(nom. – acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Fem'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative sg.
        token = "γύναι"
        expected_result = 'ἡ γυνή – γύναι!|(nom. – voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Fem'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # DUAL NUMBER
        # nominative du.
        token = "γυναῖκε"
        expected_result = 'ἡ γυνή – τὼ γυναῖκε|(sg. – du.)'
        morph = {'Case': ['Nom'], 'Gender': ['Fem'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive du.
        token = "γυναικοῖν"
        expected_result = 'ἡ γυνή – τὼ ??? – τοῖν γυναικοῖν|(sg. – du. nom. – du. gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Fem'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative du.
        token = "γυναικοῖν"
        expected_result = 'ἡ γυνή – τὼ ??? – τοῖν γυναικοῖν|(sg. – du. nom. – du. dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Fem'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative du.
        token = "γυναῖκε"
        expected_result = 'ἡ γυνή – τὼ ??? – τὼ γυναῖκε|(sg. – du. nom. – du. acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Fem'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative du.
        token = "γυναῖκε"
        expected_result = 'ἡ γυνή – τὼ ??? – γυναῖκε!|(sg. – du. nom. – du. voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Fem'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # PLURAL NUMBER
        # nominative pl.
        token = "γυναῖκες"
        expected_result = 'ἡ γυνή – αἱ γυναῖκες|(sg. – pl.)'
        morph = {'Case': ['Nom'], 'Gender': ['Fem'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive pl.
        token = "γυναικῶν"
        expected_result = 'ἡ γυνή – αἱ ??? – τῶν γυναικῶν|(sg. – pl. nom. – pl. gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Fem'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative pl.
        token = "γυναιξί"
        expected_result = 'ἡ γυνή – αἱ ??? – ταῖς γυναιξί|(sg. – pl. nom. – pl. dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Fem'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative pl.
        token = "γυναῖκας"
        expected_result = 'ἡ γυνή – αἱ ??? – τάς γυναῖκας|(sg. – pl. nom. – pl. acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Fem'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative pl.
        token = "γυναῖκες"
        expected_result = 'ἡ γυνή – αἱ ??? – γυναῖκες!|(sg. – pl. nom. – pl. voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Fem'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

    def test_neut(self):
        lemma = 'πρόσωπον'

        # SINGULAR NUMBER
        # nominative sg.
        token = "πρόσωπον"
        expected_result = self.sg_nom_msg.format(token)
        morph = {'Case': ['Nom'], 'Gender': ['Neut'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive sg.
        token = "προσώπου"
        expected_result = 'τὸ πρόσωπον – τοῦ προσώπου|(nom. – gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Neut'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative sg.
        token = "προσώπῳ"
        expected_result = 'τὸ πρόσωπον – τῷ προσώπῳ|(nom. – dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Neut'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative sg.
        token = "πρόσωπον"
        expected_result = 'τὸ πρόσωπον – τὸ πρόσωπον|(nom. – acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Neut'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative sg.
        token = "πρόσωπον"
        expected_result = 'τὸ πρόσωπον – πρόσωπον!|(nom. – voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Neut'], 'Number': ['Sing']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # DUAL NUMBER
        # nominative du.
        token = "προσώπω"
        expected_result = 'τὸ πρόσωπον – τὼ προσώπω|(sg. – du.)'
        morph = {'Case': ['Nom'], 'Gender': ['Neut'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive du.
        token = "προσώποιν"
        expected_result = 'τὸ πρόσωπον – τὼ ??? – τοῖν προσώποιν|(sg. – du. nom. – du. gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Neut'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative du.
        token = "προσώποιν"
        expected_result = 'τὸ πρόσωπον – τὼ ??? – τοῖν προσώποιν|(sg. – du. nom. – du. dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Neut'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative du.
        token = "προσώπω"
        expected_result = 'τὸ πρόσωπον – τὼ ??? – τὼ προσώπω|(sg. – du. nom. – du. acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Neut'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative du.
        token = "προσώπω"
        expected_result = 'τὸ πρόσωπον – τὼ ??? – προσώπω!|(sg. – du. nom. – du. voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Neut'], 'Number': ['Dual']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # PLURAL NUMBER
        # nominative pl.
        token = "πρόσωπα"
        expected_result = 'τὸ πρόσωπον – τά πρόσωπα|(sg. – pl.)'
        morph = {'Case': ['Nom'], 'Gender': ['Neut'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # genitive pl.
        token = "προσώπων"
        expected_result = 'τὸ πρόσωπον – τά ??? – τῶν προσώπων|(sg. – pl. nom. – pl. gen.)'
        morph = {'Case': ['Gen'], 'Gender': ['Neut'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # dative pl.
        token = "προσώποις"
        expected_result = 'τὸ πρόσωπον – τά ??? – τοῖς προσώποις|(sg. – pl. nom. – pl. dat.)'
        morph = {'Case': ['Dat'], 'Gender': ['Neut'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # accusative pl.
        token = "πρόσωπα"
        expected_result = 'τὸ πρόσωπον – τά ??? – τά πρόσωπα|(sg. – pl. nom. – pl. acc.)'
        morph = {'Case': ['Acc'], 'Gender': ['Neut'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)

        # vocative pl.
        token = "πρόσωπα"
        expected_result = 'τὸ πρόσωπον – τά ??? – πρόσωπα!|(sg. – pl. nom. – pl. voc.)'
        morph = {'Case': ['Voc'], 'Gender': ['Neut'], 'Number': ['Plur']}
        dashed_nouns, grammar_hint, info_msg = self.dashedArticledNounsComposer.compose(lemma, token, self.pos, morph)
        actual_result = self.get_actual_result(dashed_nouns, grammar_hint, info_msg)
        self.assertEqual(expected_result, actual_result)
