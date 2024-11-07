from github import Github
import os

def list_to_review_pr(repo_name):
    # Example usage
    repo_owner = "sofa-framework"
    if "GITHUB_TOKEN" in os.environ:
        github_token = os.environ['GITHUB_TOKEN']
    else:
        print("GITHUB_TOKEN environment variable is missing.")
        sys.exit(1)

    # Create a GitHub instance
    github = Github(github_token)

    # Get the repository
    repository = github.get_repo(f"{repo_owner}/{repo_name}")

    # Get all open pull requests
    pull_requests = repository.get_pulls(state='open')

    message = ""
    
    # Iterate over each pull request
    first = True
    for pull_request in pull_requests:
        # Check if the pull request has the label "pr: status to review"
        if any(label.name == 'pr: status to review' for label in pull_request.labels):
            if first == True :
                message = message + "#### " + repo_name.upper() +" PR review\n"
                first = False
            message = message + "- [#"+str(pull_request.number)+" "+str(pull_request.title)+"]("+str(pull_request.html_url)+")\n→ \n"
    
    return message
