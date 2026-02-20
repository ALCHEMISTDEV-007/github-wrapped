from collections import Counter
from datetime import datetime, timezone, timedelta

def aggregate_languages(repos):
    counter = Counter()
    for repo in repos:
        lang = repo.get("language")
        if lang:
            counter[lang] += 1
    
    total = sum(counter.values())
    lang_percentages = {}
    if total > 0:
        for lang, count in counter.most_common(5):
            lang_percentages[lang] = round((count / total) * 100)
            
    return lang_percentages

def rank_top_repos(repos, limit=3):
    def score(repo):
        stars = repo.get("stargazers_count", 0)
        updated_at = repo.get("updated_at")

        recency_bonus = 0
        if updated_at:
            try:
                updated_date = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                days_ago = (datetime.now(timezone.utc) - updated_date).days
                if days_ago <= 30:
                    recency_bonus = 5
            except ValueError:
                pass

        return (stars * 10) + recency_bonus

    if not repos:
        return []

    sorted_repos = sorted(repos, key=score, reverse=True)
    
    return [
        {
            "name": repo.get("name"),
            "stars": repo.get("stargazers_count"),
            "language": repo.get("language"),
            "updated_at": repo.get("updated_at"),
        }
        for repo in sorted_repos[:limit]
    ]


def commit_time_analysis(commits):
    hours = []
    days = set()

    for commit in commits:
        try:
            date_str = commit["commit"]["author"]["date"]
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            hours.append(dt.hour)
            days.add(dt.date())
        except (KeyError, ValueError):
            continue

    hour_counts = Counter(hours)
    total_commits = len(hours)

    night_commits = sum(count for hour, count in hour_counts.items() if hour >= 22 or hour < 5)
    morning_commits = sum(count for hour, count in hour_counts.items() if 5 <= hour < 12)
    
    # Calculate longest streak
    sorted_days = sorted(list(days))
    longest_streak = 0
    current_streak = 0
    
    if sorted_days:
        current_streak = 1
        longest_streak = 1
        for i in range(1, len(sorted_days)):
            if (sorted_days[i] - sorted_days[i-1]).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1

    return {
        "total_commits": total_commits,
        "active_days": len(days),
        "longest_streak": longest_streak,
        "commits_by_hour": dict(hour_counts),
        "night_ratio": night_commits / total_commits if total_commits > 0 else 0,
        "morning_ratio": morning_commits / total_commits if total_commits > 0 else 0
    }

def determine_personality(commit_analysis):
    commits = commit_analysis["total_commits"]
    days = commit_analysis["active_days"]
    streak = commit_analysis["longest_streak"]
    night_ratio = commit_analysis["night_ratio"]
    
    # Rarity levels: Common, Rare, Epic, Legendary, Mythic
    
    if streak >= 30 and days >= 100:
        return {"title": "Consistency King 👑", "rarity": "Legendary", "desc": "You show up every single day. A true master of habit."}
    elif commits > 1000 and days >= 50:
        return {"title": "Hardworker 🛠️", "rarity": "Epic", "desc": "You grinded out commits like there's no tomorrow."}
    elif night_ratio >= 0.6 and commits > 50:
        return {"title": "NightOwl Coder 🦉", "rarity": "Rare", "desc": "While others sleep, you build. The dark theme is your home."}
    elif commits > 300 and days < 15:
        return {"title": "Baba Yaga 🐺", "rarity": "Mythic", "desc": "Highly proficient & dangerous. You come in, ship massive features, and vanish."}
    elif commits > 0 and days < 5:
        return {"title": "Excited Kid 🚀", "rarity": "Common", "desc": "Short intense burst of commits, then silent. We all start somewhere!"}
    elif commits > 0:
        return {"title": "Casual Explorer 🧭", "rarity": "Common", "desc": "You explore code at your own pace. Keep building!"}
    else:
        return {"title": "Silent Observer 🥷", "rarity": "Common", "desc": "No commits found. Are you using a secret alt account?"}

def generate_wrapped_summary(repos, commits):
    languages = aggregate_languages(repos)
    top_repos = rank_top_repos(repos)
    commit_analysis = commit_time_analysis(commits)
    personality = determine_personality(commit_analysis)

    return {
        "languages": languages,
        "top_repos": top_repos,
        "stats": {
            "total_commits": commit_analysis["total_commits"],
            "active_days": commit_analysis["active_days"],
            "longest_streak": commit_analysis["longest_streak"]
        },
        "personality": personality
    }
