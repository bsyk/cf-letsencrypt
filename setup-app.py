import yaml
from subprocess import call

with open('domains.yml') as data_file:
    settings = yaml.safe_load(data_file)

with open('manifest.yml') as manifest_file:
    manifest = yaml.safe_load(manifest_file)

print settings
appname = manifest['applications'][0]['name']

# Push the app, but don't start it yet
call(["cf", "push", "--no-start"])

# For each domain, map a route for the specific letsencrypt check path '/.well-known/acme-challenge/'
for entry in settings['domains']:
    domain = entry['domain']
    for host in entry['hosts']:
        if host == '.':
            call(["cf", "map-route", appname, domain, "--path", "/.well-known/acme-challenge/"])
        else:
            call(["cf", "map-route", appname, domain, "--hostname", host, "--path", "/.well-known/acme-challenge/"])

# Now the app can be started
call(["cf", "start", appname])
