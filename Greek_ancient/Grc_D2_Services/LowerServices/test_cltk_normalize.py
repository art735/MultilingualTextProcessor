# from cltk.alphabet import grc
# str_mixed_greek = "παρακλίνασ᾽ ἐπέκρανεν [744] δὲ γάμου πικρὰς τελευτάς, [745] δύσεδρος καὶ δυσόμιλος [746]"
# res = grc.filter_non_greek(str_mixed_greek)
# # print(res)
#
#
# original_text = "# 1 Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ]."
# normalized_text = grc.normalize_grc(original_text)
# print(original_text)
# print(normalized_text)
from cltk.alphabet.grc import normalize_grc

# Импортирование необходимых модулей

# Пример древнегреческого текста
text = "# 1Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ [υἱοῦ θεοῦ]."

# Нормализация текста
normalized_text = normalize_grc(text)
print("Normalized Text:", normalized_text)
