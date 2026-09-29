ge_ru_dict = {
    "ა": "а",
    "ბ": "б",
    "გ": "г",
    "დ": "д",
    "ე": "е",
    "ვ": "в",
    "ზ": "з",
    "თ": "т",
    "ი": "и",
    "კ": "к",
    "ლ": "л",
    "მ": "м",
    "ნ": "н",
    "ო": "о",
    "პ": "п",
    "ჟ": "ж",
    "რ": "р",
    "ს": "с",
    "ტ": "т",
    "უ": "у",
    "ფ": "п",
    "ქ": "к",
    "ღ": "Г",
    "ყ": "кʼ",
    "შ": "ш",
    "ჩ": "ч",
    "ც": "тс",
    "ძ": "дз",
    "წ": "ц",
    "ჭ": "чʼ",
    "ხ": "х",
    "ჯ": "дж",
    "ჰ": "хʼ"
}

# text = "ქრისტე აღსდგა მკვდრეთით,\n" \
# "სიკვდილითა სიკვდილისა დამთრგუნველი\n" \
# "და საფლავების შინათა\n" \
# "ცხოვრების მიმნიჭებელი!"

text = "უფალო, შეგვიწყალენ"

result = list()
for georgian_letter in text:
    russian_letter = ge_ru_dict.get(georgian_letter)
    if russian_letter is not None:
        result.append(russian_letter)
    else:
        result.append(georgian_letter)

res = "".join(str(item) for item in result)
print(res)
