## As Ipgeolocation.io has some limitations on the use of their API, I wrote this script to trace the IP addresses of the visitors to my website.
## This script is run manually from the command line and it is not embedded in production, but for convenience data will be store in the same database as the rest of the data.
## As the database is accessible only to me and my team, I am technically not violating the terms of use of Ipgeolocation.io,
## as I am the only one using their API and I'm using it for non-commercial use as stated in their terms https://ipgeolocation.io/tos.html


## Remember to run this script manually from the command line, as it is not embedded in production.
## Remember to add IPGEOLOCATION_API_KEY to environment variables before running this script.

import os
from main.models import StartEvent
from main.post_save_checks import trace_ip


def trace():
    for event in StartEvent.objects.filter(city__isnull=True):
        trace_ip(
            event,
            IP_GEOLOCATION_SECRET_KEY=os.environ.get("IPGEOLOCATION_API_KEY", None),
        )
