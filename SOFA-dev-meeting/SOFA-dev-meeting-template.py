from datetime import date
import sys
from find_all_to_review_PR import list_to_review_pr
from list_merged_pr import list_merged_pr
from list_topics_to_be_discussed import list_topics_to_be_discussed

def postOnDiscord(message):
    # payload = {
    #     'content' : message,
    #     'username' : 'SOFA dev meeting template',
    #     'flags' : 4,
    # }
    # response = requests.post(discord_token, json=payload)
    # print("Status: "+str(response.status_code)+"\nReason: "+str(response.reason)+"\nText: "+str(response.text))
    print(message)
    return


def main(argv):
    if (len(argv) == 1):
        print("At least one repo name is required ! ")
        return

    today = date.today()
    dateToday = today.strftime("%d/%m/%Y")
    
    message="# "+str(dateToday)+"\n### News\n- \n\n### Technical discussions"
    postOnDiscord(message)

    message = list_topics_to_be_discussed("sofa")
    postOnDiscord(message)

    postOnDiscord("### PR review")
    for arg in argv[1:]:
        postOnDiscord("#### " + arg.upper() +" PR review")
        message = list_to_review_pr(arg)
        postOnDiscord(message+"\n")

    postOnDiscord("### PR merged within the week")
    for arg in argv[1:]:
        postOnDiscord("#### "+ arg.upper() +" PR merged")
        message = list_merged_pr(arg)
        postOnDiscord(message+"\n")

    postOnDiscord("\n---\n")

if __name__ == "__main__":
    main(sys.argv)
