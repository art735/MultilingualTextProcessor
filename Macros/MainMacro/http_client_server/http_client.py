# -*- coding: utf-8 -*-
import json

try:
    # Python 3
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    # Python 2
    from urllib2 import Request, urlopen, URLError, HTTPError


url = "http://localhost:5000/api/data"

def process_transcriptions(data, lang):
    payload = {"data": data, "lang": lang}
    data = json.dumps(payload).encode("utf-8")  # bytes in both versions
    # print(data)

    request = Request(url, data)
    request.add_header("Content-Type", "application/json")

    try:
        response = urlopen(request)
        response_body = response.read()

        # Ensure unicode string for JSON parsing
        if isinstance(response_body, bytes):
            response_body = response_body.decode("utf-8")

        result = json.loads(response_body)
        return result
    except HTTPError as e:
        return {"error": "HTTPError", "code": e.code, "message": str(e)}
    except URLError as e:
        return {"error": "URLError", "reason": str(e.reason)}


if __name__ == '__main__':
    data = [("[kæt]", ["[kæt]"])]
    lang = 'deu'
    res = process_transcriptions(data, lang)
    print(res)


