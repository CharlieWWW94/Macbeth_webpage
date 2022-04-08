import requests


def search(search_params):
    print(f"search param type: {search_params}. Search param[0]:{type(search_params[0])}")
    if type(search_params[0]) is tuple:
        params = {
            'theme': search_params[0][1],
            'character': search_params[1][1],
            'act': search_params[2][1],
            'scene': search_params[3][1]

        }
        print(f"search params: {search_params}")

    else:
        params = {
            'id': []
        }
        for num in search_params:
            params["id"].append(num)

    quotations = requests.get(url='http://127.0.0.1:5001/search', params=params)
    print(quotations)
    return quotations.json()
