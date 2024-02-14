# /* cSpell:disable */

import subprocess
import time

# import variance calculation
import statistics
from cik_helper import get_info_from_cik
import json
from collections import defaultdict
import os

path_to_arelle = "Arelle/arelleCmdLine.py"
path_to_brel = "examples/cli.py"
path_to_no_facts = "examples/no_facts.py"

no_runs = 10


def run_arelle(uri: str) -> float:
    start = time.time()
    subprocess.run(["python", path_to_arelle, "-f", uri])
    end = time.time()
    return end - start


def run_brel(uri: str) -> float:
    start = time.time()
    subprocess.run(["python", path_to_brel, uri])
    end = time.time()
    return end - start


def get_no_facts(uri: str) -> int:
    output = subprocess.run(["python", path_to_no_facts, uri], capture_output=True)
    return int(output.stdout.decode("utf-8"))


def test_performance(uri) -> dict:
    # call both arelle and brel once to load the cache
    run_brel(uri)
    run_arelle(uri)

    # run the two tests no_runs times and calculate the average and standard deviation
    brel_times = [run_brel(uri) for _ in range(no_runs)]
    arelle_times = [run_arelle(uri) for _ in range(no_runs)]

    brel_avg = statistics.mean(brel_times)
    arelle_avg = statistics.mean(arelle_times)

    arelle_std = statistics.stdev(arelle_times)
    brel_std = statistics.stdev(brel_times)

    # get the number of facts
    no_facts = get_no_facts(uri)

    return {
        "no_facts": no_facts,
        "brel_avg": brel_avg,
        "brel_std": brel_std,
        "arelle_avg": arelle_avg,
        "arelle_std": arelle_std,
    }


def main():
    # limit ciks for testing
    ciks = []
    with open("tests/report_tests/ciks.json", "r") as f:
        ciks = json.load(f)
    # ciks = ciks[:5]

    performance_results = defaultdict(dict)

    for cik in ciks:
        company_info = get_info_from_cik(cik, 1)
        print(company_info["company_name"])
        print(company_info["uris"])

        company_results = defaultdict(list)
        company_results["company_name"] = company_info["company_name"]
        company_results["cik"] = cik

        for uri in company_info["uris"]:
            print(f"Testing {uri}")
            results = test_performance(uri)
            print(results)

            company_results["brel_avg"].append(results["brel_avg"])
            company_results["brel_std"].append(results["brel_std"])
            company_results["arelle_avg"].append(results["arelle_avg"])
            company_results["arelle_std"].append(results["arelle_std"])
            company_results["no_facts"].append(results["no_facts"])

        performance_results[cik] = company_results

    # store the results as "performance_results.json"
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "performance_results.json")
    with open(file_path, "w") as f:
        json.dump(performance_results, f)


if __name__ == "__main__":
    main()
