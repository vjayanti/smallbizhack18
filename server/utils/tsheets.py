import requests
TSHEETS_URL = 'https://rest.tsheets.com/api/v1'
TSHEETS_KEY = 'S.7__451415bf1afd3d22321e4eeaee72c3c37d398063'

def get_users():
    tsheets = requests.get(TSHEETS_URL).content
    headers = {
        'Authorization': "Bearer "+TSHEETS_KEY,
    }
    response = requests.request("GET", TSHEETS_URL+'/users', headers=headers)
    print(response.text)
    return response.text

