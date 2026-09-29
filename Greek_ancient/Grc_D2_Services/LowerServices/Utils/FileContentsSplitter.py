# Разбивает содержимое файла на подсписки по строке с указанным разделителем (в виде callback-а). Строка файла
# добавляется в подсписок только при выполнении условия addition_condition_cb (тоже в виде callback-а).
# Например:
# 1) при парсинге TAGNT-Google-sheet с материалами к Евангелиям разделителем служит наличие фразы "Dictionary form"
# в строке текста, а условием добавления в строки в подсписок - наличие знака '=' в строке;
# 2) при парсинге Excel-листа со спряжениями немецких глаголов разделителем служит условие, чтобы самая первая ячейка
# строки была непустой, а спец. условия добавления в строки в подсписок нет (т. е. process_condition_cb пишется так,
# чтобы всегда возвращать True).
def split_file_contents_by_delimiter(file_lines, delimiter_cb, addition_condition_cb,
                                     include_line_with_delimiter_in_results=False):
    # Список списков, в котором:
    # - внутренний список - это строки, относящиеся к определённой категории (стих Евангелия, немецкий глагол)
    # - внешний список - это список внутренних списков
    results = []
    current_list = []
    started = False  # Флаг для проверки, когда начать добавление строк

    for line in file_lines:
        if delimiter_cb(line):
            if started:
                # Если разделитель найден и сбор данных уже начался,
                # добавляем текущий список в результат и начинаем новый
                if current_list:
                    results.append(current_list)
                current_list = []
            started = True  # Теперь сбор данных начался
            if include_line_with_delimiter_in_results:
                current_list.append(line)
        elif started:
            # Добавляем строку в текущий список только если сбор данных начался и выполняется условие, заданное в
            # addition_condition_cb
            if addition_condition_cb(line):
                if isinstance(line, str):
                    line = line.strip()
                current_list.append(line)

    # Добавляем последний собранный список, если он не пуст
    if started and current_list:
        results.append(current_list)

    return results
