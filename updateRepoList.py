#!/usr/bin/env python

import getpass
import sys

from collections import OrderedDict

from github_acadwf import addPyGithubToPath
from github_acadwf import getenvOrDie

addPyGithubToPath()

from github import Github
from github import GithubException

class RepoListing(object):
    def __init__(self, name, url, quarter, moderator, listOfGithubIds, description):
        self.name = name
        self.url = url
        self.quarter = quarter
        self.moderator = moderator
        self.listOfGithubIds = listOfGithubIds
        self.description = description

    

GHA_GITHUB_ORG = getenvOrDie("GHA_GITHUB_ORG",
                        "Error: please set GHA_GITHUB_ORG to name of github organization for the course, e.g. UCSB-CS56-W14")

# Authenticate to github.com and create PyGithub "Github" object
username = raw_input("Github Username:")
pw = getpass.getpass()
g = Github(username, pw, user_agent="PyGithub")

org = g.get_organization(GHA_GITHUB_ORG)

# Populate the projectCategories dictionary (a dictionary where keys are category strings and values are lists of RepoListing objects)
projectCategories = dict()
for repo in org.get_repos():
    repoName = repo.name
    repoUrl = repo.html_url
    

    
    quarter = ""
    moderator = ""
    listOfGithubIds = ""  
    description = ""
    
    # Try to pull info from the project description, where we expect format
    # quarter | moderator | team | description
    #  quarter will be "TBD" if the Repo is not yet curated for a given quarter.
    #  moderator is whoever is moderating
    #  team is "TBD" if no team assigned yet, otherwise it is a github user

    descFields = repo.description.split(' | ', 4)
    if len(descFields) == 4:
        quarter = descFields[0]
        moderator = descFields[1]
        listOfGithubIds = descFields[2]
        description = descFields[3]

    fields = repoName.split('-', 2)
    #(prefix, category, name) = repoName.split('-', 2)
    if fields[0] == "cs56" and len(fields) >= 3:
        repoCategory = fields[1].capitalize()
        repoName = fields[2]

        thisRepoListing = RepoListing(repoName, repoUrl, quarter,moderator,listOfGithubIds,description)
        if projectCategories.get(repoCategory, "") != "":
            projectCategories[repoCategory].append(thisRepoListing)
        else:
            projectCategories[repoCategory] = [thisRepoListing]
    
# Alphabetize the projectCategories dictionary and output each list of RepoListing objects alphabetically to the markdown file
alphabeticalCategories = OrderedDict(sorted(projectCategories.items(), key=lambda repoCategory: repoCategory[0]))
outputFile = open('AllRepos.md', 'w')
outputFile.write('# ' + 'CategoryList\n')

total_ready = 0
total_unclaimed = 0
for repoCategory, repoListings in alphabeticalCategories.iteritems():
    outputFile.write('\n## ' + repoCategory + '\n')
    repoListings.sort(key=lambda repoListing: repoListing.name)
    for repoListing in repoListings:
        extraInfo = ""
        if (repoListing.quarter != "") :
            extraInfo +=  ( ' %3s %10s %15s %s ' % ( repoListing.quarter,
                                             repoListing.moderator,
                                             repoListing.listOfGithubIds,
                                             repoListing.description) )
            if(repoListing.quarter.strip() == "W14") :
                total_ready += 1
                if(repoListing.listOfGithubIds.strip() == "TBD") :
                    total_unclaimed += 1

        outputFile.write('* ' + '[' + repoListing.name + '](' + repoListing.url + ') '
                         + extraInfo + '\n')
        
outputFile.write("\n## Number of Repos Ready: " + str(total_ready) + "\n## Ready and Unclaimed Repos: " + str(total_unclaimed))
outputFile.close()
    
