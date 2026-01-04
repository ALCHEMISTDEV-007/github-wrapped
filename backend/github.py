import requests

def fetch_user_repos(access_token: str):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    params = {
        "per_page": 100,
        "sort": "updated"
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()
