from collections import Counter

def aggregate_languages(repos):
    counter = Counter()
    for repo in repos:
        lang = repo.get("language")
        if lang:
            counter[lang] += 1
    return dict(counter)

#Gonna build personality logic baby!!!

from datetime import datetime
from collections import Counter
from datetime import datetime, timezone

def rank_top_repo(repos):
    def score(repo):
        stars = repo.get("stargazers_count", 0)
        updated_at = repo.get("updated_at")

        recency_bonus = 0
        if updated_at:
            updated_date = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            days_ago = (datetime.now(timezone.utc) - updated_date).days
            if days_ago <= 30:
                recency_bonus = 5

        return (stars * 10) + recency_bonus

    if not repos:
        return None

    top_repo = max(repos, key=score)
    return {
        "name": top_repo.get("name"),
        "stars": top_repo.get("stargazers_count"),
        "language": top_repo.get("language"),
        "updated_at": top_repo.get("updated_at"),
    }


def analyze_commit_times(commits):
    hours = []
    days = set()

    for commit in commits:
        date_str = commit["commit"]["author"]["date"]
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        hours.append(dt.hour)
        days.add(dt.date())

    hour_counts = Counter(hours)

    night_commits = sum(
        count for hour, count in hour_counts.items()
        if hour >= 22 or hour < 5
    )
    total_commits = len(hours)

    personality = "Balanced Coder ⚖️"
    if total_commits > 0:
        if night_commits / total_commits >= 0.6:
            personality = "Night Owl Coder 🌙"
        elif sum(
            count for hour, count in hour_counts.items()
            if 5 <= hour < 12
        ) / total_commits >= 0.6:
            personality = "Early Bird Coder ☀️"

    return {
        "total_commits": total_commits,
        "active_days": len(days),
        "commits_by_hour": dict(hour_counts),
        "personality": personality,
    }

def calculate_consistency(active_days: int):
    if active_days >= 100:
        return "HardCore Grinder🔥"
    elif active_days >= 40:
        return "Consistent Builder 🧱"
    elif active_days >=15:
        return "Casual Explorer 🧭"
    else:
        return "On & Off Learner 🌱"
