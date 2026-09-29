from CharConstants import SPACE


def process(bracketed_transcription, process_single_piece_cb):
    results = []

    pieces = [piece.strip() for piece in bracketed_transcription.split() if piece.strip()]
    for piece in pieces:
        # Данный флаг пригодится дважды:
        # 1) при стрипании '[' ДО обработки транскрипции
        # 2) при восстановлении '[' ПОСЛЕ обработки транскрипции
        is_left_bracket = piece.startswith('[')
        # Нет смысла стрипать и затем восстанавливать закрывающую квадратную скобку ']', т. к. она никак
        # не влияет на логику добавления аспирации или гортанной смычки. Здесь интересен только передний край
        # ударного слога.
        # is_right_bracket = piece.endswith(']')

        # Разумным было бы сохранить именно такой флаговый подход к обработке скобок (а не обрубать их безусловно
        # с помощью bracketed_transcription[1:-1]), т. к. если в будущем формат аргумента поменяется и на вход метода
        # будет приходить уже стрипанная от квадратных скобок транскрипция, флаговый подход будет по-прежнему работать
        # корректно, а безусловное slice-ование транскрипции может привести к потере крайних символов.
        if is_left_bracket:
            piece = piece.lstrip('[')

        # Ключевой момент обработки кусочка транскрипции
        piece = process_single_piece_cb(piece)

        # Восстанавливаем '[', если она присутствовала в оригинальной транскрипции
        if is_left_bracket:
            piece = '[' + piece

        # добавляем КАЖДЫЙ piece в results независимо от того, обрабатывался он или нет
        results.append(piece)

    output = SPACE.join(results)
    return output
