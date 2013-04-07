#!/usr/bin/python
from __future__ import print_function
import getpass
import sys

# In the main directory of the repo where you are developing with PyGithub,
# type:
#    git submodule add git://github.com/jacquev6/PyGithub.git PyGithub
#    git submodule init
#    git submodule update
#
# That will populate a PyGithub subdirectory with a clone of PyGithub
# Then, to add it to your Python path, you can do:

sys.path.append("./PyGithub");

from github import Github
from github import GithubException

orgName="UCSB-CS56-Projects"

username = raw_input("Github Username:")
pw = getpass.getpass()
g = Github(username, pw)

f = open('AllRepos.md','w')


org = g.get_organization(orgName)

repos = org.get_repos()

listOfNames=[]

for repo in repos:
    listOfNames.append(repo.name)

listOfNames.sort()

for name in listOfNames:
    print ("* {0}".format(name),file=f)

