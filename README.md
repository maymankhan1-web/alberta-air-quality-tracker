# Alberta Air Quality (AQHI) Tracker

A free, public tracker for the hourly Air Quality Health Index (AQHI) for Calgary, Edmonton and other Alberta stations.

- `fetch_data.py` (Python standard library only, no API key) downloads the data and saves it to `data/`.
- `index.html` is a static GitHub Pages site (no build step) that shows the latest values and a chart.
- A GitHub Actions workflow refreshes the data every hour and commits any changes.

Run locally: `python3 fetch_data.py`, then `python3 -m http.server` and open http://localhost:8000.

## Data attribution
Data comes from Environment and Climate Change Canada, MSC GeoMet API (api.weather.gc.ca). This project is not affiliated with or endorsed by the data provider.

## Support
If this tracker is useful to you, you can support it through [GitHub Sponsors](https://github.com/sponsors/maymankhan1-web).

## License
MIT
