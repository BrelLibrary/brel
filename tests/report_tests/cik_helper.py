import requests
import json
import os
import datetime

session = requests.Session()


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


def get_info_from_cik(cik: str, take_latest_n: int) -> dict:
    sec_data_uri = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    # print(f"Fetching {sec_data_uri}")

    # print(f"URI: {sec_data_uri}")
    sec_data = json.loads(get_from_uri(sec_data_uri))

    # print(f"Filer: {sec_data['name']} {sec_data['tickers']} {sec_data['cik']}")
    # cik_to_name[cik] = sec_data["name"]
    company_name = sec_data["name"]

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

    # ping all uris and remove the ones that are not available
    uris = []
    for accession_nr, xbrl_filename, date, form in latest_ten_qk:
        sec_xbrl_uri = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nr.replace('-', '')}/{xbrl_filename}"
        ping = requests.get(sec_xbrl_uri, headers={"User-Agent": "Mozilla/5.0"})
        # print(f"URI: {sec_xbrl_uri} Status: {ping.status_code}")
        if ping.status_code == 200:
            uris.append(sec_xbrl_uri)
        else:
            # print(f"URI {sec_xbrl_uri} is not available")
            pass

    return {"cik": cik, "company_name": company_name, "uris": uris}
