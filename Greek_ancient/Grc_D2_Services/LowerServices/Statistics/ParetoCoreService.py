# Исходим из того, что всегда интересно знать на какое количество слов/лемм приходится 80% частот частотного словаря.
# Согласно принципу Парето если мы взяли 80% частот, то должны получить 20% слов/лемм словаря,
# но в действительности этот процент оказывается существенно ниже (для Четвероевангелия, например, ниже 10%).
# Это связано с чрезмерно высокой частотой употребления артиклей, местоимений и других служебных слов.
# Их частотность оказывается существенно выше частотности "обычных" слов, и поэтому вместо ожидаемых
# 20% слов/лемм словаря, мы в реальности имеем 10% и меньше.
# Задача метода - определить реальный процент слов, на которые приходится 80% всех частот, т. е.
# другими словами: сколько иностранных слов нужно выучить, чтобы покрыть 80% всего текста.
def calculate_real_word_portion_of_pareto_80_percent_frequencies(frequency_dict):
    # Общая сумма частот
    total_frequency = sum(frequency_dict.values())

    # Порог 80% от общей суммы частот
    frequency_threshold = 0.8 * total_frequency

    # Сортировка словаря по убыванию частот
    sorted_items_list = sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)

    # cumulative ['kjuːmjələtɪv] совокупный, накопленный; интегральный, кумулятивный
    cumulative_frequency = 0
    word_count = 0

    # Проходим по отсортированному списку и суммируем частоты
    for word, freq in sorted_items_list:
        cumulative_frequency += freq
        word_count += 1
        if cumulative_frequency >= frequency_threshold:
            break

    # Рассчитываем процент ключей
    total_words = len(frequency_dict)
    word_percentage = (word_count / total_words) * 100

    return word_count, word_percentage


# Имеется частотный словарь употребления слов в тексте, отсортированный по убыванию частот.
# При этом если взять 80% суммы всех частот, она будет соответствовать не положенным 20% ключей,
# а примерно 10% или ещё меньше. Это связано с тем, что первые элементы словаря (артикли, местоимения)
# употребляются в тексте слишком часто и нарушают баланс принципа Парето 80/20.
# Нижеследующий метод считает сколько первых элементов частотного словаря, отсортированного по убыванию,
# нужно отбросить для того, чтобы найти наибольшее приближение к принципу Парето 80/20.
# Не обязательно строго 80/20, а ситуацию при которой наблюдается наибольшее приближение к этому идеалу.

# Позже вынес 20%-й порог в качестве параметра метода со значением по умолчанию = 20.
# Сделал это для того, чтобы можно было запускать метод с разными значениями этого параметра, например, 10-15-20 и
# смотреть на динамику отбрасывания слов.
# Например, для словаря Четвероевангелия 80% частот приходится на 8.2% его ключей. И было бы интересно запустить
# метод несколько раз передав в него поочерёдно значения 10-15-20 и посмотреть какой получается динамика отбрасывания
# слов для достижения идеального распределения Парето 80/20
def skip_first_n_elements_to_fit_pareto(frequency_dict, word_percentage_threshold_to_fit=20):
    # Сортировка словаря по убыванию частот с преобразованием его в СПИСОК пар {word: count}
    sorted_items_list = sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)

    best_skip_count = 0
    best_pareto_diff = float('inf')

    for skip_count in range(len(sorted_items_list)):

        # Этот срез создаёт новый список, который содержит все элементы исходного списка,
        # начиная с индекса skip_count и до конца списка
        remaining_items = sorted_items_list[skip_count:]
        remaining_items_dict = dict(remaining_items)
        word_count, word_percentage = calculate_real_word_portion_of_pareto_80_percent_frequencies(remaining_items_dict)

        # Идеальное значение = 20%
        pareto_diff = abs(word_percentage - word_percentage_threshold_to_fit)

        # Обновляем лучший результат
        if pareto_diff < best_pareto_diff:
            best_skip_count = skip_count
            best_pareto_diff = pareto_diff

    return best_skip_count

####################################

# Вычитываем файл, содержащий частотный словарь.
# Хранить частотный словарь в файле и вычитывать его практически мгновенно это намного более удачное решение, чем
# каждый раз этот словарь формировать spaCy-библиотекой (на это уходит около 6 минут времени вычислений!)
# filename_5all_gospels = '5all_four_Gospels_freq_dict.txt'
# freq_dict = FileContentsReader.read_freq_dict_from_file(filename_5all_gospels)

# word_count, word_percentage = calculate_real_word_portion_of_pareto_80_percent_frequencies(freq_dict)
# print(f'80% частот приходится на {word_percentage:.2f}% ({word_count} штук) ключей/слов/лемм словаря.')
