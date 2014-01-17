require 'io/console'
require 'octokit'

print "Enter username: "
username = gets.chomp
print "Enter password: "
pass = STDIN.noecho(&:gets).chomp
puts ''

ORG_NAME = 'UCSB-CS56-Projects'
OUTPUT   = 'repos.md'

def url_for(category, name)
  "https://www.github.com/#{ORG_NAME}/cs56-#{category}-#{name}/"
end

client      = Octokit::Client.new(login: username, password: pass)
repo_names  = client.org_repos(ORG_NAME).map(&:name)
repo_groups = Hash.new { |h,k| h[k] = [] }

repo_names.each do |name|
  next if name == "CategoryList" # Hackety hack

  _, category, *title = name.split('-')
  title = title.join('-') # Titles can have hyphens
  repo_groups[category] << title
end


File.open(OUTPUT, 'w') do |f|
  repo_groups.each do |category, repos|
    f.write "\n## #{category.capitalize}\n"

    repos.each do |name|
      url = url_for(category, name)
      f.write "* [#{name}](#{url})\n"
    end
  end
end
