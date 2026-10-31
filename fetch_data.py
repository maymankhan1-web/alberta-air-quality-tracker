#!/usr/bin/env python3
"""Fetch public data (no API key). Python standard library only."""
import json, datetime, urllib.request
def get(url, data=None, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "alberta-public-data-tracker"})
    if data is not None:
        req = urllib.request.Request(url, data=data, headers={"User-Agent": "alberta-public-data-tracker", **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as r:
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
