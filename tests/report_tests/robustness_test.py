import requests
import json
import os
import brel
import rich
from collections import defaultdict
import json

from cik_helper import get_info_from_cik


def load_results() -> dict:
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "robustness_results.json")
    with open(file_path, "r") as f:
        return json.load(f)


def store_results(results: dict) -> None:
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "robustness_results.json")
    with open(file_path, "w") as f:
        json.dump(results, f)


def uri_to_filename(uri):
    return uri.split("/")[-1]


# load ciks from ciks.json
ciks = []
with open("tests/report_tests/ciks.json", "r") as f:
    ciks = json.load(f)

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
# ciks = ciks[15:20]

for cik in ciks:
    # Get SEC Metadata from edgar for CIK
    company_info = get_info_from_cik(cik, 10)
    print(company_info["company_name"])
    cik_to_name[cik] = company_info["company_name"]

    for sec_xbrl_uri in company_info["uris"]:

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
