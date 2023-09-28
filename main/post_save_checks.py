from django.conf import settings
import requests
from datetime import datetime
import pickle
import time
import os

os.makedirs("dumps", exist_ok=True)


def dump(initiator, message, str_to_dump, object_to_dump=None, pickle_dump=True):
    if not settings.ALLOW_DUMP:
        ## If not allowed to dump
        return
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
    filename = f"dumps/{initiator}_{now}.txt"
    pickle_filename = f"dumps/{initiator}_{now}.pickle"
    with open(filename, "w") as f:
        f.write(f"[{now}] [{initiator}] {message}\n")
        f.write(str_to_dump)
        f.write("\n\n")
    if object_to_dump and pickle_dump:
        with open(pickle_filename, "wb") as f:
            pickle.dump(object_to_dump, f)


def check_captcha_token(event_instance):
    n_try = 0
    while n_try < 10:
        try:
            url = "https://www.google.com/recaptcha/api/siteverify"
            payload = {
                "secret": settings.CAPTCHA_SECRET_KEY,
                "response": event_instance.recaptcha_token,
            }
            r = requests.post(url, data=payload)

            if 200 <= r.status_code < 300:
                j = r.json()
                if j["success"]:
                    event_instance.recaptcha_score = j["score"]
                    event_instance.save()
                    return
                else:
                    print(
                        "Verification of captcha token failed", r.status_code, r.json()
                    )
                    dump(
                        "check_captcha_token",
                        "Verification of captcha token failed",
                        f"{r.status_code} {r.json()}",
                        r,
                    )
                    if n_try >= 1:
                        return
            else:
                print("Verification of captcha token failed", r.status_code, r.json())
                dump(
                    "check_captcha_token",
                    "Verification of captcha token response not ok",
                    f"{r.status_code} {r.json()}",
                    r,
                )
        except Exception as e:
            print("Verification of captcha token failed", e)
            dump(
                "check_captcha_token",
                "Verification of captcha token exception",
                str(e),
                e,
            )
        n_try += 1
        time.sleep(0.15 * n_try)


def trace_ip(
    event_instance,
    IP_GEOLOCATION_SECRET_KEY=None,
    on_error_callback=lambda *args, response, **kwargs: print(
        "IP tracing failed", response.status_code, response.json()
    ),
):
    n_try = 0
    if not IP_GEOLOCATION_SECRET_KEY and not settings.IP_GEOLOCATION_SECRET_KEY:
        print("IP tracing failed: no secret key")
        return
    while n_try < 3:
        try:
            url = ""
            params = {
                "apiKey": IP_GEOLOCATION_SECRET_KEY
                or settings.IP_GEOLOCATION_SECRET_KEY,
                "ip": event_instance.ip,
            }

            url = "https://api.ipgeolocation.io/ipgeo"
            r = requests.get(url, params=params, headers={"Accept": "application/json"})

            if 200 <= r.status_code < 300:
                j = r.json()

                event_instance.country_code = j["country_code3"]
                event_instance.country_name = j["country_name"]
                event_instance.province = j["state_prov"]
                event_instance.district = j["district"]
                event_instance.city = j["city"]
                event_instance.zipcode = str(j["zipcode"])

                event_instance.latitude = j["latitude"]
                event_instance.longitude = j["longitude"]

                event_instance.isp = j["isp"]

                event_instance.save()
                return
            else:
                on_error_callback(
                    event=event_instance, response=r, response_json=r.json()
                )
                return
        except Exception as e:
            print("IP tracing failed", e)
        n_try += 1
