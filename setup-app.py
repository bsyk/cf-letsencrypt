import yaml
from subprocess import call

with open('domains.yml') as data_file:
    settings = yaml.safe_load(data_file)

print settings

# Push the app, but don't start it yet
call(["cf", "push", "--no-start"])

# For each domain, map a route for the specific letsencrypt check path '/.well-known/acme-challenge/'
for entry in settings['domains']:
    domain = entry['domain']
    for host in entry['hosts']:
        if host == '.':
            call(["cf", "map-route", "letsencrypt", domain, "--path", "/.well-known/acme-challenge/"])
        else:
            call(["cf", "map-route", "letsencrypt", domain, "--hostname", host, "--path", "/.well-known/acme-challenge/"])

# Now the app can be started
call(["cf", "start", "letsencrypt"])
