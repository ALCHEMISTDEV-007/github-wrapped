import os
import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from github import fetch_user_repos
from analytics import aggregate_languages
from github import fetch_repo_commits
from analytics import commit_time_analysis
from analytics import calculate_consistency
from analytics import rank_top_repo
from analytics import generate_wrapped_summary


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

    # 1️⃣ Exchange code for access token
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

    # 2️⃣ Fetch user profile
    user_response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
    )
    user_data = user_response.json()

    # 3️⃣ Initialize variables (IMPORTANT)
    repos = []
    all_commits = []

    # 4️⃣ Fetch repositories
    repos = fetch_user_repos(access_token)

    # 5️⃣ Fetch commits
    for repo in repos:
        commits = fetch_repo_commits(
            owner=user_data.get("login"),
            repo=repo.get("name"),
            access_token=access_token,
        )
        all_commits.extend(commits)

    # 6️⃣ NOW generate wrapped summary (THIS is where it belongs)
    wrapped_summary = generate_wrapped_summary(repos, all_commits)

    # 7️⃣ Return everything
    return {
        "message": "GitHub Wrapped generated 🎉",
        "username": user_data.get("login"),
        "name": user_data.get("name"),
        "avatar_url": user_data.get("avatar_url"),
        "wrapped": wrapped_summary,
        "repos": repos,
    }
