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
