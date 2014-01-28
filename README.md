## Category Listing

This repo contains a script to pull all of the repos from the class organization, and format them as [Markdown](http://daringfireball.net/projects/markdown/)
for easy viewing.

### Instructions (Python Script)

The python script (updateRepoList.py) uses PyGithub.

The script prompts for the user's username and password and outputs to a markdown file titled AllRepos.md.
Make sure you have set the GHA_GITHUB_ORG environment variable to the proper organization first: 
```
export GHA_GITHUB_ORG="UCSB-CS56-Projects"
python updateRepoList.py
```

Note:
The script only lists projects whose repo names follow the following form: cs56-(category)-(projectName)
ex: cs56-games-maze, or cs56-misc-translate-to-secret-languages

### Instructions (Ruby Script)

The Ruby script requires the [Octokit](http://octokit.github.io/) gem to interact with the GitHub API. You'll need to make sure it's installed:

```
ruby -v # You should probably have 1.9.3 or higher installed
gem install octokit
ruby repos.rb
```

The script will prompt you for your GitHub credentials and write the parsed Markdown to `repos.md`.

