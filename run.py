import yaml
import os
import time
import threading
import SimpleHTTPServer
import SocketServer
from letsencrypt import main as cli

cwd = os.getcwd()
logs = cwd+"/logs"
conf = cwd+"/conf"
work = cwd+"/work"
host = cwd+"/host"

port = int(os.getenv('VCAP_APP_PORT', '5000'))

# Before we switch directories, set up our args using the domains.yml settings file.
with open('domains.yml') as data_file:
    settings = yaml.safe_load(data_file)

print(settings)

# Format commands
args = ["certonly", "--non-interactive", "--text", "--debug", "--agree-tos", "--logs-dir", logs, "--work-dir", work, "--config-dir", conf, "--webroot", "-w", host]

# Are we testing - i.e. getting certs from staging?
if 'staging' in settings and settings['staging'] is True:
    args.append("--staging")

args.append("--email")
args.append(settings['email'])

for entry in settings['domains']:
    domain = entry['domain']
    for host in entry['hosts']:
        args.append("-d")
        if host == '.':
            fqdn = domain
        else:
            fqdn = host + '.' + domain
        args.append(fqdn)

print("Args: ", args)

os.chdir('host')

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", port), Handler)

# Start a thread with the server
server_thread = threading.Thread(target=httpd.serve_forever)

# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print("Server loop listening on port ", port, ". Running in thread: ", server_thread.name)

print("Starting Let's Encrypt process in 1 minute...")

time.sleep(60)

print("Calling letsencrypt...")

cli.main(args)

print("Done.")
print("Fetch the certs and logs via cf files ...")
print("You can get them with these commands: ")
print("cf files letsencrypt app/conf/live/" + settings['domains'][0]['domain'] + "/cert.pem")
print("cf files letsencrypt app/conf/live/" + settings['domains'][0]['domain'] + "/chain.pem")
print("cf files letsencrypt app/conf/live/" + settings['domains'][0]['domain'] + "/fullchain.pem")
print("cf files letsencrypt app/conf/live/" + settings['domains'][0]['domain'] + "/privkey.pem")
print()
print("REMEMBER TO STOP THE SERVER WITH cf stop letsencrypt")

# Sleep for a week
time.sleep(604800)

print("Done.  Killing server...")

# If we kill the server and end, the DEA should restart us and we'll try to get certificates again
httpd.shutdown()
httpd.server_close()
