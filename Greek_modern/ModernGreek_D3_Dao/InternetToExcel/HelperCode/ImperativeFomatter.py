def capitalize_and_add_exclamation_mark(verb):
    if len(verb) > 0:
        result = verb.strip().capitalize() + '!'
    else:
        result = '–'

    return result
