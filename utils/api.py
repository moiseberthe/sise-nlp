import requests
from env import CLIENT_ID, CLIENT_SECRET


def get_pole_emploi_access_token():
    url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api_offresdemploiv2"
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']