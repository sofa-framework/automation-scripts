from datetime import date
import sys
from find_all_to_review_PR import list_to_review_pr
from list_merged_pr import list_merged_pr

def main(argv):
    if (len(argv) == 1):
        print("At least one repo name is required ! ")
        return

    today = date.today()
    dateToday = today.strftime("%d/%m/%Y")
    print("# "+str(dateToday))

    print("### News")
    print("- ")
    print("")
    print("### Technical discussions")
    print("- ")
    print("")

    print("### PR review")
    for arg in argv[1:]:
        print("#### " + arg.upper() +" PR review")
        list_to_review_pr(arg)
        print("")

    print("### PR merged within the week")
    for arg in argv[1:]:
        print("#### "+ arg.upper() +" PR merged")
        list_merged_pr(arg)
        print("")

    print("---")
    print("")

if __name__ == "__main__":
    main(sys.argv)
