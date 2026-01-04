from collections import Counter

def aggregate_languages(repos):
    counter = Counter()
    for repo in repos:
        lang = repo.get("language")
        if lang:
            counter[lang] += 1
    return dict(counter)
