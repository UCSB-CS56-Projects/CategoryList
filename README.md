## Category Listing

This repo contains a script to pull all of the repos from the class organization, and format them as [Markdown](http://daringfireball.net/projects/markdown/)
for easy viewing.

### Instructions

The Ruby script requires the [Octokit](http://octokit.github.io/) gem to interact with the GitHub API. You'll need to make sure it's installed:

```
ruby -v # You should probably have 1.9.3 or higher installed
gem install octokit
ruby repos.rb
```

The script will prompt you for your GitHub credentials and write the parsed Markdown to `repos.md`.

