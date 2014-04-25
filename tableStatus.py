#!/usr/bin/env python

import getpass
import sys

from collections import OrderedDict

from github_acadwf import addPyGithubToPath
from github_acadwf import getenvOrDie

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
    
    print "Processed: " + repo.description

print "Number of Repos Approved: " + str(approvedCount)
print "Number of Repos Unapproved: " + str(unapprovedCount)
print "Number of Repos Not Yet Evaluated " + str(notYetEvaluated) 
print "Number processed by Adam: " + str(moderatorCount["mastergberry"])
print "Number processed by Bronwyn: " + str(moderatorCount["bronhuston"])
    
