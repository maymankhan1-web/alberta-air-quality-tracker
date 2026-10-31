#!/usr/bin/env python3
"""Fetch public data (no API key). Python standard library only."""
import json, datetime, urllib.request
import sys, time, socket, urllib.error

RETRY_DELAYS = (5, 15, 30)


def _retryable(err):
    if isinstance(err, urllib.error.HTTPError):
        return err.code == 429 or err.code >= 500
    return isinstance(err, (urllib.error.URLError, TimeoutError, socket.timeout, ConnectionError))


def urlopen_retry(req, timeout=60):
    """Open a URL, retrying temporary upstream errors. Exits cleanly if the source stays down."""
    for attempt in range(len(RETRY_DELAYS) + 1):
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except Exception as err:
            if not _retryable(err):
                raise
            if attempt == len(RETRY_DELAYS):
                print(f"Source unavailable after {attempt + 1} attempts ({err}); keeping existing data.")
                sys.exit(0)
            print(f"Attempt {attempt + 1} failed ({err}); retrying in {RETRY_DELAYS[attempt]}s")
            time.sleep(RETRY_DELAYS[attempt])

def get(url, data=None, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "alberta-public-data-tracker"})
    if data is not None:
        req = urllib.request.Request(url, data=data, headers={"User-Agent": "alberta-public-data-tracker", **(headers or {})})
    with urlopen_retry(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
import csv
CITIES = ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Medicine Hat", "Grande Prairie", "Fort McMurray"]
out = {}
for c in CITIES:
    url = ("https://api.weather.gc.ca/collections/aqhi-observations-realtime/items?f=json&limit=48&sortby=-observation_datetime&location_name_en="
           + urllib.request.quote(c))
    fs = get(url)["features"]
    out[c] = sorted([{"time": f["properties"]["observation_datetime"], "aqhi": f["properties"]["aqhi"]} for f in fs], key=lambda r: r["time"])
json.dump({"updated": NOW, "source": "ECCC MSC GeoMet", "stations": out}, open("data/latest.json","w"), indent=1)
with open("data/aqhi_recent.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["station","time_utc","aqhi"])
    for c, rs in out.items():
        for r in rs: w.writerow([c, r["time"], r["aqhi"]])
print({c: (rs[-1] if rs else None) for c, rs in out.items()})
