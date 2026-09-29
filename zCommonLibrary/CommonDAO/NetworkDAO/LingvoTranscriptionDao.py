import json
import time

import requests

# from importlib.machinery import SourceFileLoader
# txtDao = SourceFileLoader('TxtDao', '../LocalDAO/TxtDao.py').load_module()

# Should be requested at https://developers.lingvolive.com
apiKey1 = 'ZTFlYjJkZTQtY2NlZC00Y2Q4LThlZjktOGEyMjk1YmI0NmZjOmQ5ZDAxODY1ZjJkMjRmMjE4N2ZhZDY3NmE1NWI0M2Y5'
apiKey2 = 'MzRhNjk5NWEtOTM2ZC00ZDAzLWFkYjMtYWVjNjIxNjFjYTNkOjMxYmE3OTNjN2JkNTRkZDdiZjU5OTI5NDlmNGY3ZjA4'
apiKey3 = 'Y2JkMjg5ZGUtOTM0Yi00NjZlLWI0ZTgtZTM5YTg4NDNkMTY2OmVhODhhYWExZWNiNjQ0MDBiZTVlZDE2OWYyOGUwMzc4'
apiKey4 = 'ZTJkNzQ3NDQtNGIyNy00MDBiLWE3NDgtZTM1ODlkMDZjMTk1OjEzYWJkNDgxODk0YzQ0NjliNjVmMzU4ZWQ2YjYzMDBk'

apiKey = apiKey4

BASE_LINGVO_URL = 'https://developers.lingvolive.com'

url_1 = BASE_LINGVO_URL + '/api/v1.1/authenticate'
headers_1 = {'Authorization': 'Basic {}'.format(apiKey)}

token = ""


def _postApiKeyToGetAuthToken(url, requestHeaders):
    # POST request
    r = requests.post(url, headers=requestHeaders)
    token = r.text
    return token


def _getUrl(wordToLookUp):
    # LingvoUniversal (En-Ru) 1033 → 1049
    # обязательно прямой slash в начале строки перед словом api
    url = BASE_LINGVO_URL + '/api/v1/Article?heading={heading}&dict={dict}&srcLang={srcLang}&dstLang={dstLang}'.format(
        heading=wordToLookUp, dict="LingvoUniversal%20(En-Ru)", srcLang="1033", dstLang="1049")
    return url


def _processMarkupJsonPiece(json_piece_dict):
    transcription = json_piece_dict['Markup'][0]['Text']
    return transcription


def get_transcription(word, delay_between_requests):
    # global variable name 'token' is included
    global token

    if token == "":
        token = _postApiKeyToGetAuthToken(url_1, headers_1)

    url_2 = _getUrl(word)
    headers_2 = {'Authorization': 'Bearer {}'.format(token)}

    # GET request
    response = requests.get(url_2, headers=headers_2)
    time.sleep(delay_between_requests)  # после риспонса подождать несколько секунд, прежде чем делать следующий

    response_json = json.loads(response.text)

    try:
        # transcription = ""
        body_0_dict = response_json['Body'][0]
        if body_0_dict.get('Markup') is not None:
            transcription = _processMarkupJsonPiece(body_0_dict)
        else:
            transcription = _processMarkupJsonPiece(body_0_dict['Items'][1]['Markup'][0])
    except Exception:
        transcription = "NOT_FOUND"
        time.sleep(delay_between_requests * 2)  # wait two times longer that usual

    return "[{}]".format(transcription)

##################

# words = ["cat", "schedule", "encompass", "from"]
# words = ["from"]
# words = TxtDao.readLinesFromFile(r'e:\Languages\English\SVN repo\Python software\MultilingualTextProcessor\resources\numerals.txt')
#
# delay_between_requests = 2  # delay between requests (in seconds)
#
# for word in words:
#     transcription = get_transcription(word, delay)
#     output = f"{word} {transcription}".format(word, transcription)
#     print(output)
