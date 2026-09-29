# -*- coding: utf-8 -*-
import sys

# base_path = r'E:\Languages\English\SVN repo\Python software\MultilingualTextProcessor\Macros'
#
# def import_paths(self):
#     subfolders = self._get_subfolders(base_path)
#     for subfolder in subfolders:
#         if all(path_piece not in subfolder for path_piece in [r'\.idea', r'\resources', r'\test']):
#             if subfolder not in sys.path:
#                 sys.path.append(subfolder)
#             # print(subfolder)
#
# # Получить список всех подпапок в указанной директории
# # Пути к ПАПКАМ, содержащим импортируемые модули, но не fullpath самих модулей!
# def _get_subfolders(self, directory):
#     subfolders = []
#     for root, dirs, _ in os.walk(directory):
#         for dir_name in dirs:
#             subfolder_name = os.path.join(root, dir_name)
#             if not subfolder_name.endswith("__pycache__"):  # папки __pycache__ игнорируется
#                 subfolders.append(subfolder_name)
#     return subfolders

base_path = r'E:\Languages\English\SVN repo\Python software\MultilingualTextProcessor\Macros'

sys.path.append(base_path + r'\MainMacro')
sys.path.append(base_path + r'\SimpleNppAndOfficeMacro\Presentation_office')


#########################################

import A1_PythonMacroMainModule
import text_replacer_office_macro

def run_main_macro():
    doc = XSCRIPTCONTEXT.getDocument()
    A1_PythonMacroMainModule.run(doc)

def run_simple_npp_and_office_macro():
    doc = XSCRIPTCONTEXT.getDocument()
    text_replacer_office_macro.run(doc)

