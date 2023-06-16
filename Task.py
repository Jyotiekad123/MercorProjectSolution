import requests
import re

def fetch_user_repositories(github_url):
    username = extract_username(github_url)
    api_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(api_url)
    repositories = response.json()
    return repositories

def extract_username(github_url):
    pattern = r"github\.com/([^/]+)"
    match = re.search(pattern, github_url)

    if match:
        username = match.group(1)
    else:
        username = None

    return username

def find_most_recent_repository(repositories):
    most_recent_repository = None
    recent_commit_timestamp = ""

    for repository in repositories:
        commits_url = repository["commits_url"].split("{")[0]
        commits_response = requests.get(commits_url)
        commits = commits_response.json()
        
        if commits and isinstance(commits, list) and "commit" in commits[0]:
            commit_timestamp = commits[0]["commit"]["committer"]["date"]
            if commit_timestamp > recent_commit_timestamp:
                recent_commit_timestamp = commit_timestamp
                most_recent_repository = repository

    return most_recent_repository

if __name__ == "__main__":
    github_url = input("Enter GitHub user URL: ")
    repositories = fetch_user_repositories(github_url)
    most_recent_repository = find_most_recent_repository(repositories)
    print("Most recent repository:", most_recent_repository["name"])
    print("URL:", most_recent_repository["html_url"])
