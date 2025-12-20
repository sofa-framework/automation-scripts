import os
import sys
import requests
from datetime import date
from find_all_to_review_PR import list_to_review_pr
from list_merged_pr import list_merged_pr
from list_topics_to_be_discussed import list_topics_to_be_discussed

discord_token = os.environ['DISCORD_WEBHOOK_URL']

def postOnDiscord():
    file = {'file': open('SOFA-dev-meeting.txt','rb')}
    response = requests.post(discord_token, files=file)
    print("Status: "+str(response.status_code)+"\nReason: "+str(response.reason)+"\nText: "+str(response.text))
    return


def main(argv):
    if (len(argv) == 1):
        print("At least one repo name is required ! ")
        return

    today = date.today()
    dateToday = today.strftime("%d/%m/%Y")
    
    message="# "+str(dateToday)+"\n### News\n- \n\n### Technical discussions\n"

    output = list_topics_to_be_discussed("sofa-framework","sofa")
    message = message + output + "\n"

    message = message + "### PR review\n"
    for arg in argv[1:]:
        repo_owner = "sofa-framework"
        repo_name = arg
        if "/" in arg:
            repo_owner = arg.split("/")[0]
            repo_name = arg.split("/")[1]
        output = list_to_review_pr(repo_owner, repo_name)
        if output != "":
            message = message + output +"\n"

    message = message + "### PR merged within the week\n"
    for arg in argv[1:]:
        repo_owner = "sofa-framework"
        repo_name = arg
        if "/" in arg:
            repo_owner = arg.split("/")[0]
            repo_name = arg.split("/")[1]
        output = list_merged_pr(repo_owner, repo_name)
        if output != "":
            message = message + output +"\n"

    message = message + "\n---\n"
    
    with open("SOFA-dev-meeting.txt", "w") as f:
        f.write(message)

    postOnDiscord()


if __name__ == "__main__":
    main(sys.argv)
