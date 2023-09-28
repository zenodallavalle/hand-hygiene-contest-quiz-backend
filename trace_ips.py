## As Ipgeolocation.io has some limitations on the use of their API, I wrote this script to trace the IP addresses of the visitors to my website.
## This script is run manually from the command line and it is not embedded in production, but for convenience data will be store in the same database as the rest of the data.
## As the database is accessible only to me and my team, I am technically not violating the terms of use of Ipgeolocation.io,
## as I am the only one using their API and I'm using it for non-commercial use as stated in their terms https://ipgeolocation.io/tos.html


## Remember to run this script manually from the command line, as it is not embedded in production.
## Remember to add IPGEOLOCATION_API_KEY to environment variables before running this script.

from itertools import islice, repeat
import os
from threading import Thread

from main.models import StartEvent
from main.post_save_checks import trace_ip

n_thread = 10


def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def trace_multiple_ips(start_events, api_key, on_error_callback):
    for start_event in start_events:
        trace_ip(start_event, api_key, on_error_callback)


def on_error_callback(*args, event, response, response_json, **kwargs):
    message = response_json.get("message", "")
    if not message:
        print("IP tracing failed", response.status_code, response_json)
        return
    if "private-use" in message.lower():
        print("Private IP address, setting Milan as city for IP: {}".format(event.ip))
        # As the site is accessed from a private IP it means is inside the local network, so the city will be Milan
        event.city = "Milan"
        event.latitude = 45.46796
        event.longitude = 9.18178
        event.save()
        return
    print("IP tracing failed", response.status_code, message)


def trace():
    start_events = list(StartEvent.objects.filter(city__isnull=True, ip__isnull=False))
    chunks = batched(start_events, len(start_events) // n_thread)
    if not chunks:
        print("No IP to trace")
        return
    threads = []
    for chunk in chunks:
        t = Thread(
            target=trace_multiple_ips,
            args=(chunk, os.environ["IPGEOLOCATION_API_KEY"], on_error_callback),
        )
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("Done")
