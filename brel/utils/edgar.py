"""
This module is a helper for the SEC EDGAR database. It provides a function to download filings from the SEC EDGAR database given the CIK and the filing type.
If a date is provided, the function will download the filing for the given date. If no date is provided, the function will download the most recent filing.

The module also provides a function for listing all filings for a given CIK and filing type.
"""

from brel import Filing
import requests, json, os, datetime

SUPPORTED_FILING_TYPES = ["10-K", "10-Q", "8-K"]

session = requests.Session()

# the edgar cache dir is in the user's home directory in .brel_edgar_cache
# create the directory if it does not exist
if not os.path.exists(os.path.join(os.path.expanduser("~"), ".brel_edgar_cache")):
    os.makedirs(os.path.join(os.path.expanduser("~"), ".brel_edgar_cache"))
edgar_cache_dir = os.path.join(os.path.expanduser("~"), ".brel_edgar_cache")


def __download_metadata_for_cik(cik: str) -> bool:
    """
    Downloads the file for the cik and places it in the edgar cache dir.
    :param cik: The CIK of the company.
    :return: True if the metadata was downloaded successfully, False otherwise.
    """
    print(f"Downloading metadata for CIK {cik}")
    sec_data_uri = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"

    response = session.get(sec_data_uri, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return False

    response_json = response.json()
    with open(os.path.join(edgar_cache_dir, f"{cik.zfill(10)}.json"), "w") as f:
        json.dump(response_json, f)

    return True


def __is_cached(cik: str) -> bool:
    """
    Checks if the metadata for the given CIK is cached.
    :param cik: The CIK of the company.
    :return: True if the metadata is cached, False otherwise.
    """
    return os.path.exists(os.path.join(edgar_cache_dir, f"{cik.zfill(10)}.json"))


def open_edgar(cik: str, filing_type: str, date: str | None = None) -> Filing:
    """
    Download a filing from the SEC EDGAR database given the CIK and the filing type.

    Example usage:
    ```
    from brel.utils import open_edgar

    # The cik for Apple Inc.
    apple_cik = "320193"
    report_type = "10-K"
    filing = open_edgar(apple_cik, report_type)
    ```

    Alternatively, you can specify a date to download a filing for a specific date.
    Use the format YYYY-MM-DD for the date.

    Example usage:

    ```
    from brel.utils import open_edgar

    filing = open_edgar("320193", "10-K", "2021-01-01")
    ```

    Note that the date refers to the report date, not the filing date.

    :param cik: The CIK of the company.
    :param filing_type: The filing type. Has to be one of the following: "10-K", "10-Q", "8-K".
    :param download_dir: The directory where the filing will be downloaded.
    :param date: The date of the filing in the format YYYY-MM-DD.
    :return: The path to the downloaded filing.
    """

    # check that the date is in the correct format
    if date is not None:
        if not isinstance(date, str):
            raise ValueError("The date has to be a string in the format YYYY-MM-DD")
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect date format. The date has to be in the format YYYY-MM-DD")

    # check that the cik is a str that has at most 10 characters
    if not isinstance(cik, str) or len(cik) > 10:
        raise ValueError("The CIK has to be a string with at most 10 characters")

    # Check if the filing type is supported
    if filing_type not in SUPPORTED_FILING_TYPES:
        raise ValueError(
            f"Filing type {filing_type} is not supported. It has to be one of the following: {', '.join(SUPPORTED_FILING_TYPES)}"
        )

    # Check if the metadata for the CIK is cached
    if not __is_cached(cik):
        if not __download_metadata_for_cik(cik):
            raise ValueError(f"Failed to download metadata for CIK {cik}")
    else:
        # if the file is older than 1 day, download it again
        if (
            datetime.datetime.now()
            - datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(edgar_cache_dir, f"{cik.zfill(10)}.json")))
        ).days > 1:
            if not __download_metadata_for_cik(cik):
                raise ValueError(f"Failed to download metadata for CIK {cik}")

    # Load the metadata for the CIK
    with open(os.path.join(edgar_cache_dir, f"{cik.zfill(10)}.json"), "r") as f:
        metadata = json.load(f)

        recent = metadata["filings"]["recent"]

        def report_fits(i: int) -> bool:
            is_right_type = recent["form"][i] == filing_type
            is_xbrl = str(recent["isXBRL"][i]) == "1"
            is_right_date = date is None or recent["reportDate"][i] == date
            return is_right_type and is_xbrl and is_right_date

        right_is = [i for i in range(len(recent["form"])) if report_fits(i)]

        right_is.sort(key=lambda i: int(recent["reportDate"][i].replace("-", "")), reverse=True)

        right_i = right_is[0] if len(right_is) > 0 else None

        if right_i is None:
            raise ValueError(f"No filing found for CIK {cik}, filing type {filing_type}, and date {date}")

        accession_number = recent["accessionNumber"][right_i]
        primary_doc = recent["primaryDocument"][right_i]

        uri = (
            f"https://www.sec.gov/Archives/edgar/data/{cik.zfill(10)}/{accession_number.replace('-', '')}/{primary_doc}"
        )

        if uri.endswith(".htm"):
            uri_dir = uri[: uri.rfind("/")]
            uri = uri.replace(".htm", "_htm.xml")
            ping = session.get(uri, headers={"User-Agent": "Mozilla/5.0"})
            if ping.status_code != 200:
                raise ValueError(
                    f"Failed to download filing from {uri}. Note that the Brel does not support .htm filings and that it cannot scrape EDGAR's website. We suggest that you search for the .xml filing on {uri_dir} and call brel.Filing.open(uri) with the correct URI."
                )
        print(f"Opening {filing_type} filing of {metadata['name']} ({cik}) on {recent['reportDate'][right_i]}")
        return Filing.open(uri)
