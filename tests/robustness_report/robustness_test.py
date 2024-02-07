import requests
import json
import os
import brel
import datetime
import rich
from collections import defaultdict
import json


def load_results() -> dict:
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "results.json")
    with open(file_path, "r") as f:
        return json.load(f)


def store_results(results: dict) -> None:
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "results.json")
    with open(file_path, "w") as f:
        json.dump(results, f)


def uri_to_filename(uri):
    return uri.split("/")[-1]


def get_from_uri(uri):
    file_name = uri_to_filename(uri)
    file_path = f"edgar_cache/{file_name}"
    is_cached = os.path.isfile(file_path)
    if is_cached:
        # print("Loading from cache")
        with open(file_path, "r") as f:
            return f.read()
    else:
        # a bit hacky but the SEC blocks bots so we need to spoof a user agent
        response = session.get(uri, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            # print message
            print(f"SEC data request failed with {response.text}")
            raise Exception(
                f"SEC data request failed with status code {response.status_code}"
            )
        # store in cache as a new file
        with open(file_path, "w") as f:
            f.write(response.text)
        return response.text


ciks = [
    # 1. Microsoft
    "0000789019",
    # 2. Apple
    "0000320193",
    # 3. Alphabet (Google)
    "0001652044",
    # 4. Amazon
    "0001018724",
    # 5. Nvidia
    "0001045810",
    # 6. Meta (Facebook)
    "0001326801",
    # 7. Berkshire Hathaway
    "0001067983",
    # 8. Eli Lilly
    "0000059478",
    # 9. Tesla
    "0001318605",
    # 10. Broadcom
    "0001730168",
    # 11. Visa
    "0001403161",
    # 12. JP Morgan
    "0000019617",
    # 13. United Health
    "0000731766",
    # 14. Walmart
    "0000104169",
    # 15. Exxon Mobil
    "0000034088",
    # 16. Mastercard
    "0001141391",
    # 17. Johnson & Johnson
    "0000200406",
    # 18. Procter & Gamble
    "0000080424",
    # 19. Home Depot
    "0000354950",
    # 20. Oracle
    "0001341439",
    # 21. Merck
    "0000310158",
    # 22. Costco
    "0000909832",
    # 23. AbbVie
    "0001551152",
    # 24. AMD
    "0000002488",
    # 25. Chevron
    "0000093410",
    # 26. Adobe
    "0000796343",
    # 27. Salesforce
    "0001108524",
    # 28. Bank of America
    "0000070858",
    # 29. Coca-Cola
    "0000021344",
    # 30. Netflix
    "0001065280",
    # 31. PepsiCo
    "0000077476",
    # 32. Thermo fisher
    "0000097745",
    # 33. mcDonalds
    "0000063908",
    # 34. cisCo
    "0000858877",
    # 35. abbott
    "0001800008",
    # 36. t-mobile us
    "0001283699",
    # 37. Danaher
    "0000313616",
    # 38. Intel
    "0000050863",
    # 39. Intuit
    "0000896878",
    # 40. Comcast
    "0001166691",
    # 41. Disney
    "0001001039",
    # 42. Wells Fargo
    "0000072971",
    # 43. Verizon
    "0000732712",
    # 44. Amgen
    "0000318154",
    # 45. IBM
    "0000051143",
    # 46. Caterpillar
    "0000018230",
    # 47. ServiceNow
    "0001373715",
    # 48. Qualcomm
    "0000804328",
    # 49. Nike
    "0000320187",
    # 50. Union Pacific
    "0000100885",
]

reports_per_year = ["10-Q", "10-K"]
take_latest_n = 10

session = requests.Session()

total_reports = 0
total_errors = 0
total_crashes = 0
total_success = 0

crashes_per_cik: dict[str, int] = defaultdict(int)
errors_per_cik: dict[str, int] = defaultdict(int)
success_per_cik: dict[str, int] = defaultdict(int)
cik_to_name: dict[str, str] = defaultdict(str)

# crop the cik list for testing
# ciks = ciks[:20]

for cik in ciks:
    # Get SEC Metadata from edgar for CIK
    sec_data_uri = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    print(f"Fetching {sec_data_uri}")

    # print(f"URI: {sec_data_uri}")
    sec_data = json.loads(get_from_uri(sec_data_uri))

    print(f"Filer: {sec_data['name']} {sec_data['tickers']} {sec_data['cik']}")
    cik_to_name[cik] = sec_data["name"]

    recent = sec_data["filings"]["recent"]

    # get the accessionNumber of all recent 10-Q and 10-K filings
    ten_qk = [
        (
            recent["accessionNumber"][i],
            recent["primaryDocument"][i].replace(".htm", "_htm.xml"),
            datetime.datetime.strptime(recent["filingDate"][i], "%Y-%m-%d"),
            recent["form"][i],
        )
        for i, f in enumerate(recent["form"])
        if f == "10-Q" or f == "10-K"
    ]

    ten_k = [x for x in ten_qk if x[3] == "10-K"]
    ten_q = [x for x in ten_qk if x[3] == "10-Q"]

    # latest_ten_qk = sorted(ten_qk, key=lambda x: x[2], reverse=True)[:take_latest_n]
    latest_ten_qk = (
        sorted(ten_k, key=lambda x: x[2], reverse=True)[:take_latest_n]
        + sorted(ten_q, key=lambda x: x[2], reverse=True)[:take_latest_n]
    )

    for accession_nr, xbrl_filename, date, form in latest_ten_qk:
        # print(f"{accession_nr} {xbrl_filename} {date}")
        sec_xbrl_uri = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nr.replace('-', '')}/{xbrl_filename}"
        print(f"> [{form} {date.date()}] {sec_xbrl_uri}")

        # ping the uri to see if it's available. Otherwise skip the testcase
        ping = requests.get(sec_xbrl_uri, headers={"User-Agent": "Mozilla/5.0"})
        if ping.status_code == 404:
            print(f"Not found. Skipping")
            continue

        # Load filing from URI
        try:
            filing = brel.Filing.open(sec_xbrl_uri)
            errors = filing.get_errors()
            if len(errors) > 0:
                errors_per_cik[cik] += 1
                total_errors += 1

                rich.print(
                    f"[yellow] {len(errors)} errors or warnings in {sec_xbrl_uri}"
                )
                for error in errors:
                    print(f"Error: {error}")
            else:
                total_success += 1
                success_per_cik[cik] += 1
        except Exception as e:
            print(f"Failed to load filing from {sec_xbrl_uri}")
            total_crashes += 1
            crashes_per_cik[cik] += 1
        total_reports += 1

rich.print("[bold]Summary[/bold]")
rich.print(f"Total reports: {total_reports}")
rich.print(f"{len(ciks)} companies, {take_latest_n} reports each")
rich.print(f"[green]Success, [yellow]Errors, [red]Crashes")

bar_symbol = "█"

print()
rich.print(
    f"[green]{bar_symbol * total_success}[yellow]{bar_symbol * total_errors}[red]{bar_symbol * total_crashes}"
)
rich.print(
    f"Reports: {total_reports}, Success: {total_success}, Errors: {total_errors}, Crashes: {total_crashes}"
)
print()
rich.print("Individual company results")

for cik, name in cik_to_name.items():
    cik_crashes = crashes_per_cik.get(cik, 0)
    cik_errors = errors_per_cik.get(cik, 0)
    cik_success = success_per_cik.get(cik, 0)
    cik_total = cik_crashes + cik_errors + cik_success
    rich.print(f"[bold]{name} ({cik})[/bold]")
    # rich.print(f"[green]{bar_symbol * cik_success}[red]{bar_symbol * cik_crashes}")
    rich.print(
        f"[green]{bar_symbol * cik_success}[yellow]{bar_symbol * cik_errors}[red]{bar_symbol * cik_crashes}"
    )
    rich.print(
        f"Reports: {cik_total}, Success: {cik_success}, Errors: {cik_errors}, Crashes: {cik_crashes}"
    )
    print()

results_dict = {
    "total_reports": total_reports,
    "total_success": total_success,
    "total_errors": total_errors,
    "total_crashes": total_crashes,
    "crashes_per_cik": crashes_per_cik,
    "errors_per_cik": errors_per_cik,
    "success_per_cik": success_per_cik,
    "cik_to_name": cik_to_name,
}

store_results(results_dict)
