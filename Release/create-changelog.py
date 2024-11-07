#!python

# DEPENDENCIES
# python3 -m pip install python-graphql-client

# REFERENCES
# How to request: https://stackoverflow.com/questions/42021113/how-to-use-curl-to-access-the-github-graphql-api
# Discussions API: https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions
# Pagination tuto: https://til.simonwillison.net/github/graphql-pagination-python

import os
import sys
import json
from datetime import datetime, timedelta, date
from python_graphql_client import GraphqlClient

if(len(sys.argv) != 2):
    if(len(sys.argv) > 2):
      print("Only one argument is expected")
    else:
      print("One argument expected\n - targeted_release_milestone (e.g. \"v23.12\")")
    exit(1)

# Recover input data
targeted_release_milestone=sys.argv[1]


def subtract_six_months(input_string):
    year = int(input_string[1:3]) # Extracting year
    month = int(input_string[4:6]) # Extracting month
    
    # Subtracting 6 months
    new_month = month - 6
    new_year = year
    
    # Adjusting year if month goes below 1
    if new_month <= 0:
        new_month += 12
        new_year -= 1
    
    # Format the new date as "vYY.MM" string
    new_string = "v{:02d}.{:02d}".format(new_year, new_month)
    return new_string

# Deduce previous version subtracting 6 months
previous_version = subtract_six_months(targeted_release_milestone)


client = GraphqlClient(endpoint="https://api.github.com/graphql")
github_token = os.environ['GITHUB_TOKEN']


def make_query_PR_for_milestone(owner, name, after_cursor=None):
    query = """
      query {
        repository(owner: "%s" name: "%s") {
          pullRequests(first: 10, after:AFTER) {
            totalCount
            pageInfo {
              hasNextPage
              endCursor
            } 
            nodes {
              labels(first:10) {
                edges {
                  node {
                    name
                  }
                }
              }
              title
              number
              permalink
              merged
              milestone {
                title
              }
            }
          }
        }
      }""" % (owner, name)
    return query.replace("AFTER", '"{}"'.format(after_cursor) if after_cursor else "null")



has_next_page = True
after_cursor = None

# Sort PRs according to their labels, the ordering is done as follows:
#   - PR: highlighted in next release
#   - PR: breaking
#   - PR: fix
#   - PR: cleaning

#Initialize output strings
highlighted_string=""
breaking_string=""
improvements_string=""
fix_string=""
cleaning_string=""
refactoring_string=""
others_string=""

#Buffer variables
PR_title=""
milestone_title=""
PR_number=0
PR_permalink=""
labels_list=[]

print("============================")
print("Target milestone is: "+targeted_release_milestone)
print("============================")

counter=0

while has_next_page:
    data = client.execute(
        query = make_query_PR_for_milestone("sofa-framework", "sofa", after_cursor),
        headers = {"Authorization": "Bearer {}".format(github_token)},
    )

    totalPR = data["data"]["repository"]["pullRequests"]["totalCount"]

    # For each discussion
    for node in data["data"]["repository"]["pullRequests"]["nodes"]:
      
      counter=counter+1
      print("{:.1f} %\r".format(counter/totalPR*100), end =" ")


      if node["milestone"] != None :

        PR_title = node["title"]
        milestone_title = node["milestone"]["title"]

        # print(PR_title)
        # print(milestone_title)

        if(milestone_title == targeted_release_milestone):

          if (node["labels"] != None) and (node["merged"] == True) :

            # print(PR_title)

            labels_list=[]

            for labels in node["labels"]["edges"]:
              labels_list.append(labels["node"]["name"])

            # print(labels_list)

            if "pr: highlighted in next release" in labels_list:
              highlighted_string=highlighted_string+"- "+str(node["title"])+" [#"+str(node["number"])+"]("+str(node["permalink"])+") \n"
            elif "pr: breaking" in labels_list:
              breaking_string=breaking_string+"- "+str(node["title"])+" [#"+str(node["number"])+"]("+str(node["permalink"])+") \n"
            elif ("enhancement" in labels_list) or ("pr: new feature" in labels_list):
              improvements_string=improvements_string+"- "+str(node["title"])+" [#"+str(node["number"])+"]("+str(node["permalink"])+") \n"
            elif "pr: fix" in labels_list:
              fix_string=fix_string+"- "+str(node["title"])+" [#"+str(node["number"])+"]("+str(node["permalink"])+") \n"
              # print("-------- IS FIX !!! --------")
            elif "pr: clean" in labels_list:
              cleaning_string=cleaning_string+"- "+str(node["title"])+" [#"+str(node["number"])+"]("+str(node["permalink"])+") \n"
            elif "refactoring" in labels_list:
              refactoring_string=refactoring_string+"- "+str(node["title"])+" [#"+str(node["number"])+"]("+str(node["permalink"])+") \n"
            else :
              others_string=others_string+"- "+str(node["title"])+" [#"+str(node["number"])+"]("+str(node["permalink"])+") \n"


    # save if request has another page to browse and its cursor pointers
    has_next_page = data["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
    after_cursor = data["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]



# Create filename
filename = "CHANGELOG-"+str(targeted_release_milestone)+".md"

# Erase possible existing content
open(str(filename), 'w').close()

# Start writing
file = open(str(filename), "a")
file.write("# SOFA Changelog\n\n\n\n")
file.write("## ["+str(targeted_release_milestone)+".00]( https://github.com/sofa-framework/sofa/tree/"+str(targeted_release_milestone)+".00 )\n\n")
file.write("[Full log]( https://github.com/sofa-framework/sofa/compare/"+str(previous_version)+".."+str(targeted_release_milestone)+" )\n\n")

file.write("### Highlighted contributions\n\n")
file.write(str(highlighted_string)+"\n\n")

file.write("### Breaking\n\n")
file.write(str(breaking_string)+"\n\n")

file.write("### Improvements\n\n")
file.write(str(improvements_string)+"\n\n")

file.write("### Bug Fixes\n\n")
file.write(str(fix_string)+"\n\n")

file.write("### Cleaning\n\n")
file.write(str(cleaning_string)+"\n\n")

file.write("### Refactoring\n\n")
file.write(str(refactoring_string)+"\n\n")

file.write("### Others\n\n")
file.write(str(others_string)+"\n\n")

file.close()

print("File \'"+str(filename)+"\' generated.")