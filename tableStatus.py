#!/usr/bin/env python

import getpass

from github_acadwf import addPyGithubToPath


def writeRepoHelper(outputFile, repoTitle, repos):
    outputFile.write("##" + repoTitle + "\n")
    outputFile.write("| Repo | Moderator | Description |\n")
    outputFile.write("| ---- | --------- | ----------- |\n")
    for repo in repos:
        descFields = repo.description.split(' | ')
        if len(descFields) == 2:
            continue
        description = descFields[3] if len(descFields) >= 4 else descFields[2]
        outputFile.write("| [" + repo.name.split('-', 2)[2] + "](" + repo.url + ") | " + descFields[1].lower() + " | " + description + " |\n")
    outputFile.write("\n")

addPyGithubToPath()

from github import Github
from github import GithubException   

# Authenticate to github.com and create PyGithub "Github" object
username = raw_input("Github Username:")
pw = getpass.getpass()
g = Github(username, pw, user_agent="PyGithub")

org = g.get_organization("UCSB-CS56-Projects")
moderatorCount = {"mastergberry": 0, "bronhuston": 0}
approvedCount = 0
unapprovedCount = 0
notYetEvaluated = 0

repos = dict(approved=dict(), denied=dict(), unprocessed=dict())
badRepos = []
outputFile = open('ReposStatus.md', 'w')

# Populate the projectCategories dictionary (a dictionary where keys are category strings and values are lists of RepoListing objects)
projectCategories = dict()
for repo in org.get_repos():
    # Try to pull info from the project description, where we expect format
    # YES/NO/? | mastergberry/bronhuston | {1-2 more sections}
    # YES = Ready for W15 atm
    # NO = Not suitable for W15 atm
    # ? = Not yet processed
    descFields = repo.description.split(' | ')

    # Some bad data that we want to ignore
    if len(descFields) < 2:
        continue

    status = descFields[0].lower()
    moderator = descFields[1].lower()
    
    if status == "yes":
        approvedCount += 1
    elif status == "no":
        unapprovedCount += 1
    elif status == "?":
        notYetEvaluated += 1
        
    if moderator == "mastergberry" or moderator == "bronhuston":
        moderatorCount[moderator] += 1

    print("Processed: " + repo.description)

    if len(descFields) == 2:
        badRepos.append(repo)
        continue

    nameParts = repo.name.split('-')
    if len(nameParts) < 3:
        badRepos.append(repo)
        continue

    key = ""
    if status == "yes":
        key = "approved"
    elif status == "no":
        key = "denied"
    elif status == "?":
        key = "unprocessed"
    else:
        badRepos.append(repo)
        continue

    if nameParts[1] not in repos[key]:
        repos[key][nameParts[1]] = []
    repos[key][nameParts[1]].append(repo)

# Generate our MD file now
outputFile.write("#Approved Repos\n")
for title, repoList in repos['approved'].items():
    writeRepoHelper(outputFile, title, repoList)

outputFile.write("#Denied Repos\n")
for title, repoList in repos['denied'].items():
    writeRepoHelper(outputFile, title, repoList)

outputFile.write("#Unprocessed Repos\n")
for title, repoList in repos['unprocessed'].items():
    writeRepoHelper(outputFile, title, repoList)

outputFile.write("#Ignored Repos\n")
outputFile.write("| Repo Name |\n")
outputFile.write("| --------- |\n")
for repo in badRepos:
    outputFile.write("| " + repo.name + " |\n")

outputFile.close()

print("Number of Repos Approved: " + str(approvedCount))
print("Number of Repos Unapproved: " + str(unapprovedCount))
print("Number of Repos Not Yet Evaluated " + str(notYetEvaluated))
print("Number processed by Adam: " + str(moderatorCount["mastergberry"]))
print("Number processed by Bronwyn: " + str(moderatorCount["bronhuston"]))
