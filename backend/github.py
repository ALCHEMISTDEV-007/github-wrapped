import requests

def fetch_user_repos(access_token: str):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    params = {
        "per_page": 100,
        "sort": "updated",
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()


def fetch_repo_commits(owner: str, repo: str, access_token: str, per_page=100):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    params = {
        "per_page": per_page,
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return []

    return response.json()
