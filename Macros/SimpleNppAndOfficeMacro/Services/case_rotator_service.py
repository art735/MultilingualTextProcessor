def rotate_case(text):
    text_stripped = text.strip()

    if not text_stripped:
        return text  # ничего не меняем, если строка пустая

    if text_stripped.isupper():
        result = text.lower()
    elif text_stripped.islower():
        result = text.title()
    else:
        result = text.upper()

    return result


###########################################################

if __name__ == '__main__':
    # Примеры
    print(rotate_case("HELLO WORLD"))   # hello world
    print(rotate_case("hello world"))   # Hello World
    print(rotate_case("Hello World"))   # HELLO WORLD
    print(rotate_case("   "))           # (пустая строка)
