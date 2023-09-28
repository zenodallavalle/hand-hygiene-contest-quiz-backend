## As Ipgeolocation.io has some limitations on the use of their API, I wrote this script to trace the IP addresses of the visitors to my website.
## This script is run manually from the command line and it is not embedded in production, but for convenience data will be store in the same database as the rest of the data.
## As the database is accessible only to me and my team, I am technically not violating the terms of use of Ipgeolocation.io,
## as I am the only one using their API and I'm using it for non-commercial use as stated in their terms https://ipgeolocation.io/tos.html


## Remember to run this script manually from the command line, as it is not embedded in production.
## Remember to add IPGEOLOCATION_API_KEY to environment variables before running this script.

import os
from main.models import StartEvent
from main.post_save_checks import trace_ip


def on_error_callback(*args, event, response_json, **kwargs):
    message = response_json.get("message", "")
    if not message:
        return
    if "private-use" in message.lower():
        # As the site is accessed from a private IP it means is inside the local network, so the city will be Milan
        event.city = "Milan"
        event.latitude = 45.46796
        event.longitude = 9.18178
        event.save()


def trace():
    for event in StartEvent.objects.filter(city__isnull=True, ip__isnull=False):
        trace_ip(
            event,
            IP_GEOLOCATION_SECRET_KEY=os.environ.get("IPGEOLOCATION_API_KEY", None),
        )
