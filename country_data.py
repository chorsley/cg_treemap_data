"""
Usage:
    country_data.py --json_file=<json_file> --risk_type=<risk_type> \
                    --date_filter=<date_filter>

Options:
    -f, --json_file=<s>     JSON data to load for processing
    -r, --risk_type=<s>     Risk type to filter on
    -d, --date_filter=<s>   ISO date (yyyy-mm-dd) to filter on
"""

from docopt import docopt
import json
import csv
import pprint


COUNTRY_FILE = "country-codes.csv"

CONTINENT_MAP = {
    "AS": "Asia",
    "NA": "N America",
    "SA": "S America",
    "OC": "Oceania",
    "AF": "Africa",
    "EU": "Europe",
    "": "Unknown",
    "AN": "Antarctica",
}

ARGS = {}


def load_countries():
    countries = {}

    with open(COUNTRY_FILE, "rt", encoding='utf-8') as f:
        cr = csv.DictReader(f)
        for row in cr:
            countries[row["ISO3166-1-Alpha-2"].lower()] = {
                "continent": CONTINENT_MAP[row["Continent"]],
                "name": row["name"],
            }

    return countries


def process(raw, countries):
    grouped = []

    for rec in sorted(raw, key=lambda v: v["country"]):
        if (
            rec["risk"] == ARGS["--risk_type"] and
            rec["date"] == ARGS["--date_filter"]
        ):
            cc = rec.get("country")
            cc_data = countries.get(cc)

            if cc and cc_data:
                continent = cc_data.get("continent")
                count = int(rec.get("count"))
                grouped.append([cc, continent, count])
            else:
                # import sys
                # sys.stderr.write("{}\n".format(rec))
                pass
    return grouped


if __name__ == "__main__":
    ARGS = docopt(__doc__)

    countries = load_countries()

    with open(ARGS["--json_file"], "rt") as f:
        raw = json.load(f)
        pprint.pprint({
            "meta": {
                "risk": ARGS["--risk_type"],
                "date": ARGS["--date_filter"]
            },
            "data": process(raw, countries)
        })
