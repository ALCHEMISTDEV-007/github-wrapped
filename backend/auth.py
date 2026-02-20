import os
import requests
import json
import urllib.parse
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from github import fetch_user_repos
from analytics import aggregate_languages
from github import fetch_repo_commits
from analytics import (
    generate_wrapped_summary
)
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
    # 1. Exchange code for token
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
        return {
            "error": "OAuth failed",
            "details": token_data
        }

    # 2. Fetch user
    user_headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    user_data = requests.get("https://api.github.com/user", headers=user_headers).json()

    # 3. Fetch repos + commits
    repos = fetch_user_repos(access_token)
    all_commits = []
    for repo in repos:
        commits = fetch_repo_commits(
            owner=user_data["login"],
            repo=repo["name"],
            access_token=access_token,
        )
        all_commits.extend(commits)

    # 4. Generate wrapped
    wrapped_summary = generate_wrapped_summary(repos, all_commits)

    # 5. Redirect to frontend (ONE WAY)
    payload = {
        "username": user_data["login"],
        "avatar_url": user_data["avatar_url"],
        "wrapped": wrapped_summary,
    }

    encoded = urllib.parse.quote(json.dumps(payload))

    return RedirectResponse(
        url=f"http://localhost:5173/wrapped.html?data={encoded}",
        status_code=302
    )
