from github import Github
import os

def list_topics_to_be_discussed(repo_owner, repo_name):
    if "GITHUB_TOKEN" in os.environ:
        github_token = os.environ['GITHUB_TOKEN']
    else:
        print("GITHUB_TOKEN environment variable is missing.")
        sys.exit(1)

    # Create a GitHub instance
    github = Github(github_token)

    # Get the repository
    repository = github.get_repo(f"{repo_owner}/{repo_name}")
    
    message = ""

    # ------------------------------------------------

    # Get all open issues (and PR, since PR are compatible with issues for GitHub)
    issues = repository.get_issues(state='open')

    # Iterate over each issues
    for issue in issues:
        # Check if the issue has the label "pr: status to review"
        if any(label.name == 'topic for next dev-meeting' for label in issue.labels):
            message = message + "- [#"+str(issue.number)+" "+str(issue.title)+"]("+str(issue.html_url)+")\n"

    # ------------------------------------------------

    return message
