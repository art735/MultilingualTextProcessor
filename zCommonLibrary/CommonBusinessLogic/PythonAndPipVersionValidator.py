import os
import platform

import pip
from jproperties import Properties


def _get_recommended_version_from_config(option_name):
    app_config_filename = r'E:\Languages\[Git repo] MultilingualTextProcessor\app-config.properties'

    app_config = Properties()
    with open(app_config_filename, 'rb') as config_file:
        app_config.load(config_file)
    app_config_value_by_key = app_config.get(option_name).data
    return app_config_value_by_key


def _get_real_python_version_from_runtime():
    python_version = platform.python_version()
    # print(python_version)
    return python_version


def validate_python_version():
    # Вычитываем из config-файла версию Python-интерпретатора, на котором по идее должна запускаться программа
    app_config_python_version = _get_recommended_version_from_config("python.version")

    # Узнаём реальную версию Python-интерпретатора, на котором реально стартует программа
    platform_python_version = _get_real_python_version_from_runtime()

    if app_config_python_version != platform_python_version:
        validation_msg = (f'Real Python version ({platform_python_version}) and'
                          f' .properties-file Python version ({app_config_python_version}) don\'t coincide!')
        print(validation_msg)


def validate_pip_version():
    # Вычитываем из config-файла версию pip
    app_config_pip_version = _get_recommended_version_from_config("pip.version")

    # Узнаём реальную версию pip
    installed_pip_version = pip.__version__

    if app_config_pip_version != installed_pip_version:
        validation_msg = (f'Real pip version ({installed_pip_version}) and'
                          f' .properties-file Python version ({app_config_pip_version}) don\'t coincide!')
        print(validation_msg)


# E.g. for Python 3.11.9 -> PYTHONHOME=C:\Program Files\Python311
def validate_PYTHONHOME_environment_variable():
    PYTHONHOME_env_var_key = 'PYTHONHOME'

    # Если в системе существует переменная среды PYTHONHOME_env_var_key
    if PYTHONHOME_env_var_key in os.environ:
        # Шаг 1. Вычитываем из операционной системы значение переменной PYTHONHOME_env_var_key
        actual_PYTHONHOME_env_var_value = os.environ.get(PYTHONHOME_env_var_key)

        # Шаг 2. Конструируем ожидаемое значение переменной PYTHONHOME_env_var_key исходя из реально работающей версии Python
        runtime_python_version = _get_real_python_version_from_runtime()
        # E.g. for Python 3.11.9 -> major=3, minor=11, patch=9
        pieces = runtime_python_version.split('.')
        major = pieces[0]
        minor = pieces[1]
        # patch = pieces[2]

        expected_PYTHONHOME_env_var_value = f'C:\Program Files\Python{major}{minor}'

        if expected_PYTHONHOME_env_var_value != actual_PYTHONHOME_env_var_value:
            print(
                f"Версия запущенного Python-интерпретатора не соответствует настройкам переменной среды '{PYTHONHOME_env_var_key}'")
    else:
        print(f"В операционной системе отсутствует переменная среды '{PYTHONHOME_env_var_key}'")


def validate():
    validate_python_version()
    validate_PYTHONHOME_environment_variable()
    validate_pip_version()

######################################################


# validate()
