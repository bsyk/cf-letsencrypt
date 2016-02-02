# cf-letsencrypt
Let's Encrypt wrapper for Cloud-Foundry

Create certificates for your Cloud-Foundry-hosted apps and domains using [Let's Encrypt](https://letsencrypt.org).

Using the `--path` argument of the map-route command, you can specify just a path to be directed to a separate app.

```
NAME:
   map-route - Add a url route to an app

USAGE:
   cf map-route APP_NAME DOMAIN [--hostname HOSTNAME] [--path PATH]

EXAMPLES:
   cf map-route my-app example.com                              # example.com
   cf map-route my-app example.com --hostname myhost            # myhost.example.com
   cf map-route my-app example.com --hostname myhost --path foo # myhost.example.com/foo

OPTIONS:
   --hostname, -n   Hostname for the route (required for shared domains)
   --path           Path for the route
```

Firstly you must have your cf cli configured, domains created, and DNS configured to point to your CF provider.

Once you have that, just edit the domains.yml file checked out from this repo and run `python setup-app.py`.

This will push the app, map all the routes for the auto-check that LetsEncrypt needs to do to verify that you own the domain.
It maps host.domain/.well-known/acme-challenge to this app for each domain/host that you want to generate a certificate for.

The LetsEncrypt client will sign the requests, go through the verification and fetch the signed certificates that you can then fetch with the cf files command.

Just watch the logs to see when the process has finished. `cf logs letsencrypt`

While you could leave the app running, it probably makes sense to stop it when you don't need it, and just start it up when you need to renew certificates or add another host/domain.
By default it will keep running for 1 week, then kill itself.  DEA will then try to restart it for you...
