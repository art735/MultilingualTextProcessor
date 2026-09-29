import TimeUtils
from AnkiConnectService import AnkiConnectService

ankiConnectService = AnkiConnectService()


def create_deck_hierarchy(taskNumber):
    deck_names = [
        "Занятие {0}".format(taskNumber),
        "Занятие {0}::S1. Слова [?]".format(taskNumber),
        "Занятие {0}::S2. Средняя часть [?]".format(taskNumber),
        "Занятие {0}::S2. Средняя часть [?]::1. Спряжение глаголов".format(taskNumber),
        "Занятие {0}::S2. Средняя часть [?]::2. Выражения".format(taskNumber),
        "Занятие {0}::S2. Средняя часть [?]::3. Грамматика".format(taskNumber),
        "Занятие {0}::S3. Упражнения [?]".format(taskNumber),
        "Занятие {0}::S3. Упражнения [?]::Упражнение 1".format(taskNumber),
        "Занятие {0}::S3. Упражнения [?]::Упражнение 2".format(taskNumber),
        "Занятие {0}::S3. Упражнения [?]::Упражнение 3".format(taskNumber),
        "Занятие {0}::S3. Упражнения [?]::Упражнение 4".format(taskNumber),
        "Занятие {0}::S3. Упражнения [?]::Упражнение 5".format(taskNumber)
    ]

    for deck_name in deck_names:
        ankiConnectService.create_deck(deck_name)

    # end of method


#####################################

TimeUtils.print_current_timestamp()

taskNumber = "7.1"
create_deck_hierarchy(taskNumber)

TimeUtils.print_current_timestamp()
