import TimeUtils

########################

# TimeUtils.get_current_timestamp()

# Пример создания дека
# invokeAnkiConnect('createDeck', deck='test1')


# Вывести на экран список деков
# result = invokeAnkiConnect('deckNames')
# for res in result:
#     print(res)


# Gets the complete list of deck names and their respective IDs for the current user
# deckNamesAndIds_dict = invokeAnkiConnect('deckNamesAndIds')
# print(deckNamesAndIds_dict)

# for deckName, deckId in deckNamesAndIds_dict.items():
#     # print(f'{deckName} -> {deckId}'.format(deckName, deckId))
#     notes = invokeAnkiConnect('findNotes', query=f'deck:{deckName}'.format(deckName))
#     print(notes)

# deckName = '1. Буквы и звуки'
# notes = invokeAnkiConnect('findNotes', query=f'deck:{deckName}'.format(deckName))
# notes = invokeAnkiConnect('findNotes', query="deck:test")

# deck_name = "test"
# notes = getNotesByDeckName(deck_name)
# for note in notes:
#     # front = note['fields']['Front']['value']
#     # print(front)
#     findNotesWithNonMatchingNumberOfLineBreaks(note)


# for deckName in invokeAnkiConnect('deckNames'):
#     print(deckName)


###################################################################
# allNotes_dict = getAllNotesFromAllDecks()
#
# # Unpack dict values to a flat list
# # allNotes_dict.values() returns nested list (list of lists)
# notes = list(itertools.chain(*allNotes_dict.values()))
#
# for note in notes:
#     findNotesWithNonMatchingNumberOfLineBreaks(note)

#####################

# # Get note types names via AnkiConnect API
# modelNames = AnkiConnectDao.invokeAnkiConnect('modelNames')
# for n in modelNames:
#     print(n)

# Convert list of note types names into dictionary
# my_dict = {modelNames[i]: 0 for i in range(0, len(modelNames))}

# allNotes_dict = getAllNotesFromAllDecks()
# notes = getNotesByDeckName("Музыка")
# notes = getNotesByDeckName("Georgian. [...] жил-был я")
# notes = getNotesByDeckName("French. !Words (done)")
# notes = getNotesByDeckName("Deutsch. Goethe Institute A1 Wordlist")

# for deck, notes in allNotes_dict.items():
#     for note in notes:
#         note_model_name = note['modelName']
#         my_dict[note_model_name] += 1

####################
# for deckName in invokeAnkiConnect('deckNames'):
#     print("Processing " + deckName + "...")
#     notes = getNotesByDeckName(deckName)
#     for note in notes:
#         note_model_name = note['modelName']
#         my_dict[note_model_name] += 1
###########################

####################
# for deckName in ['Deutsch. !Words (done)', 'Deutsch. !Words (new)', 'Deutsch. !Попов. Словарь', 'Deutsch. VS-es, collocations, sentences, texts', 'French. !Words (done)']:
#     print("################################################################")
#     print("### " + deckName + " ###")
#     print("################################################################")
#     notes = getNotesByDeckName(deckName)
#     for note in notes:
#         findNotesWithNonMatchingNumberOfLineBreaks(note)

###########################

# for k, v in my_dict.items():
#     print(f'{k}: {v}'.format(k, v))

# for note_id in notes_ids:
#     note = invokeAnkiConnect('notesInfo', query=note_id)
