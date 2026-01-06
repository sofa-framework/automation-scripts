import requests
from datetime import datetime, timedelta
import os

def get_merged_pull_requests(repo_owner, repo_name, token):
    base_url = "https://api.github.com"
    headers = {"Authorization": f"Bearer {token}"}
    merged_pull_requests = []

    # Get the date from last week
    last_week = datetime.now() - timedelta(weeks=1)
    last_week_str = last_week.strftime("%Y-%m-%dT%H:%M:%S")

    # Get the list of pull requests
    url = f"{base_url}/repos/{repo_owner}/{repo_name}/pulls?state=closed&sort=updated&direction=desc"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pull_requests = response.json()

        # Filter pull requests merged since last week
        for pull_request in pull_requests:
            merged_at = pull_request["merged_at"]
            if merged_at and merged_at > last_week_str:
                merged_pull_requests.append(pull_request)

    return merged_pull_requests


def list_merged_pr(repo_owner, repo_name):
    if "GITHUB_TOKEN" in os.environ:
        github_token = os.environ['GITHUB_TOKEN']
    else:
        print("GITHUB_TOKEN environment variable is missing.")
        sys.exit(1)

    merged_pull_requests = get_merged_pull_requests(repo_owner, repo_name, github_token)

    message = ""
    
    if merged_pull_requests:
        message = message + "#### " + repo_name.upper() +" PR merged\n"

    # Print the merged pull requests
    for index, pull_request in enumerate(merged_pull_requests, start=1):
        message = message + "- [#"+str(pull_request['number'])+" "+str(pull_request['title'])+"]("+str(pull_request['html_url'])+")\n"

    return message
