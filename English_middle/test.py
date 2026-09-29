import nltk
from nltk import word_tokenize

text = word_tokenize("And now for something completely different")
res = nltk.pos_tag(text)
print(res)

# nltk.help.upenn_tagset()
