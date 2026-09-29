set PYTHONUTF8=1

REM pip install -r "%~dp0\requirements_2_spacy_lang_packages.txt"

REM В requirements-файле нельзя прописать команду python -m spacy download el_core_news_lg, поэтому что все прописываемые там инструкции предназначены для pip. Данная команда прописывается здесь.
python -m spacy download el_core_news_lg

pause