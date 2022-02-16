import requests


def search(search_params):
    params = {
        'theme': search_params[0][1],
        'character': search_params[1][1],
        'act': search_params[2][1],
        'scene': search_params[3][1]

    }
    print(params)
    quotations = requests.get(url='http://127.0.0.1:5001/search', params=params)
    print(quotations)
    return quotations.json()
