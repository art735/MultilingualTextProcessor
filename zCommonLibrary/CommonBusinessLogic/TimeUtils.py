from datetime import datetime


def get_current_timestamp():
    return datetime.now().strftime("%H:%M:%S")


def print_current_timestamp():
    print(get_current_timestamp())


if __name__ == '__main__':
    print_current_timestamp()
