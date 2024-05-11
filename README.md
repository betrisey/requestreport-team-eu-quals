# requestreport - Team Europe 2024 quals

## Description
Introducing requestreport 📨🚨, a beginner-friendly XSS challenge. Its built-in request bin allows you to exfiltrate flags without any setup.

After rumors of a tulip 🌷 backdoor, I carefully compartmentalized all services built by members of Team Europe. So, even if there was a backdoor granting RCE, it would not be possible to retrieve the flag with it.

URL: https://requestreport-136-243-41-145.traefik.me/app

## Provided files
None, only the URL because the "report" page contains the source of the XSS bot and no substantial changes were made to requestrepo (only frontend changes to be able to host it in a subfolder).

## Setup
Update the IP of the server in `.env`:
```
DOMAIN=requestreport-136-243-41-145.traefik.me
IP=136.243.41.145
```

```bash
docker compose up --build
```

## Solution
Update the `DOMAIN` environment variable in `solution/compose.yaml`, then run `docker compose up --build` in the `solution` directory.
