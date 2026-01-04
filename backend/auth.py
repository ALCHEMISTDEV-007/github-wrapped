import os
import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from github import fetch_user_repos


load_dotenv()  # 👈I had a problem fetching client id& THIS IS My FIX

router = APIRouter()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

@router.get("/login")
def login():
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        "&scope=read:user"
    )
    return RedirectResponse(github_auth_url)

@router.get("/callback")
def callback(code: str):
    # 1. Exchange code for access token
    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
    }
    headers = {"Accept": "application/json"}

    token_response = requests.post(token_url, data=payload, headers=headers)
    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return {"error": "Failed to get access token"}

    # 2. Fetch user profile
    user_api_url = "https://api.github.com/user"
    user_headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    user_response = requests.get(user_api_url, headers=user_headers)
    user_data = user_response.json()

    # 3. Fetch repositories
    repos = fetch_user_repos(access_token)

    # 4. Return everything together
    return {
        "message": "GitHub profile + repos fetched 🎉",
        "username": user_data.get("login"),
        "name": user_data.get("name"),
        "avatar_url": user_data.get("avatar_url"),
        "followers": user_data.get("followers"),
        "repos_count": len(repos),
        "repos": [
            {
                "name": repo.get("name"),
                "stars": repo.get("stargazers_count"),
                "language": repo.get("language"),
                "updated_at": repo.get("updated_at"),
            }
            for repo in repos
        ],
    }

