from django.conf import settings
import requests


def check_captcha_token(event_instance):
    n_try = 0
    while n_try < 3:
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
                print("Verification of captcha token failed", r.status_code, r.json())
        except Exception as e:
            print("Verification of captcha token failed", e)
        n_try += 1


def trace_ip(event_instance):
    n_try = 0
    if not settings.IP_GEOLOCATION_SECRET_KEY:
        print("IP tracing failed: no secret key")
        return
    while n_try < 3:
        try:
            url = ""
            params = {
                "apiKey": settings.IP_GEOLOCATION_SECRET_KEY,
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
                print("IP tracing failed", r.status_code, r.json())
        except Exception as e:
            print("IP tracing failed", e)
        n_try += 1
