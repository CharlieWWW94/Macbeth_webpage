import os

import requests


def search(search_params):
    if type(search_params[0]) is tuple:
        params = {
            'theme': search_params[0][1],
            'character': search_params[1][1],
            'act': search_params[2][1],
            'scene': search_params[3][1]

        }

    else:
        params = {
            'id': []
        }
        for num in search_params:
            params["id"].append(num)

    quotations = requests.get(url='http://127.0.0.1:5001/search', params=params, headers={'key': os.getenv("API_KEY")})
    return quotations.json()
