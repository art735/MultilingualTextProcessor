# -*- coding: utf-8 -*-
import uno
import os
import subprocess

import UnoUtils

python3_path = r"C:\Program Files\Python311\python.exe"
multilingual_text_processor = r'E:\Languages\English\SVN repo\Python software\MultilingualTextProcessor'

methods_and_paths_dict = {
    "find_in_text_bracketed_transcriptions_and_process_them": multilingual_text_processor + r'\zCommonLibrary\CommonBusinessLogic\transcription_modifiers\processors\T0_TranscriptionProcessorsController.py'
}


def run_python3_script(method_name):
    if method_name not in methods_and_paths_dict:
        UnoUtils.show_messagebox("Error", 'Method with such a name in not added to dict: ' + method_name)
        return

    script_path = methods_and_paths_dict[method_name]

    # Копируем переменные окружения и удаляем из них те, которые связаны с Python3 для корректной работы Python2.
    # Поскольку работаем копией переменных окружения, реальные переменные никак не страдают.
    try:
        env = os.environ.copy()
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONPATH", None)
        env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.Popen(
            [python3_path, script_path, method_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )

        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf-8').strip()
        stderr = stderr.decode('utf-8').strip()

        result = stdout if stdout else stderr

        # show_messagebox("Result", result)
        return result

    except Exception as e:
        show_messagebox("Error", unicode(str(e), 'utf-8') if isinstance(e, str) else str(e))


