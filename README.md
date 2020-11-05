# Spider generator for DoemBaseSpider

These scripts generate spiders for [Querido Diario](https://github.com/okfn-brasil/querido-diario), more specifically DoemBaseSpider, which crawls Diarios Oficiais as part of the [DOEM platform](https://www.doem.org.br)

- File `00_check_cities.py` will go through the list of cities available on http://www.ibdm.org.br and check which ones respond 200 and which ones respond with a redirect
  - Requests that return 200 (no redirects) are stored at `cities_ok.csv`
  - Requests that cause a redirect are stored on `cities_redirect.csv`
  - Requests that didn't respond with 200 are stored on `cities_error.csv`
- File `01_create_spiders.py` will match the successful cities with the territory IDs from `territories.csv` and for the cities that have a match, generate a spider file using `spider_template.txt` as a template

## To-Do:

- Check each URL on cities_ok.csv to see if the gazettes hosted there are current (some cities dropped, or never used, the DOEM platform)
