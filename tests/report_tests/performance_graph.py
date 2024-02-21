# /* cSpell:disable */
import os
import json
import pandas as pd
from collections import defaultdict
from matplotlib import pyplot as plt
import matplotlib


def load_results_dataframe():
    current_dir = os.path.dirname(__file__)
    results_path = os.path.join(current_dir, "performance_results.json")
    results = json.load(open(results_path, "r"))

    df_dict = defaultdict(list)
    speedups = []
    times_brel = []
    times_arelle = []
    stds_brel = []
    stds_arelle = []
    no_reports = 0

    for cik, info in results.items():
        name = info["company_name"]
        if "no_facts" not in info:
            continue
        for i in range(len(info["no_facts"])):
            no_facts = info["no_facts"][i]
            brel_avg = info["brel_avg"][i]
            brel_std = info["brel_std"][i]
            arelle_avg = info["arelle_avg"][i]
            arelle_std = info["arelle_std"][i]

            df_dict["company"].append(name)
            df_dict["no_facts"].append(no_facts)
            df_dict["brel_avg"].append(brel_avg)
            df_dict["brel_std"].append(brel_std)
            df_dict["arelle_avg"].append(arelle_avg)
            df_dict["arelle_std"].append(arelle_std)

            speedup = brel_avg / arelle_avg
            speedups.append(speedup)
            times_brel.append(brel_avg)
            times_arelle.append(arelle_avg)
            stds_brel.append(brel_std)
            stds_arelle.append(arelle_std)
            no_reports += 10

    df = pd.DataFrame(df_dict)
    print(f"average speedup: {sum(speedups) / len(speedups):.2f}")
    print(f"average time brel: {sum(times_brel) / len(times_brel):.2f}")
    print(f"average std brel: {sum(stds_brel) / len(stds_brel):.2f}")
    print(f"average time arelle: {sum(times_arelle) / len(times_arelle):.2f}")
    print(f"average std arelle: {sum(stds_arelle) / len(stds_arelle):.2f}")
    print(f"number of reports: {no_reports}")
    return df


def plot_performance_graph(df, save_path):
    plt.style.use("seaborn-v0_8-darkgrid")

    plt.figure(figsize=(6, 4))
    plt.errorbar(
        df["no_facts"], df["brel_avg"], yerr=df["brel_std"], fmt="o", label="BREL"
    )
    plt.errorbar(
        df["no_facts"], df["arelle_avg"], yerr=df["arelle_std"], fmt="o", label="Arelle"
    )

    # make the x axis log scale with base 2
    plt.xscale("log", base=2)
    # same for y axis
    # write the ticks on the y axis as decimal numbers
    plt.yscale("log", base=2)
    # get all y tick,s
    plt.yticks(ticks=[1, 2, 4], labels=["1", "2", "4"])
    yticks = plt.yticks()[0]
    yticks = yticks[0:-1]
    print(yticks)
    # write the y ticks as powers of 2. write them as ints
    # plt.yticks(yticks, [f"{2**x}" for x in yticks])
    # plt.yticks(yticks, [f"{2**x:.0f}" for x in yticks])

    plt.title("Report loading time per number of facts")
    plt.xlabel("Number of facts in report")
    plt.ylabel("Loading Time (s)")
    plt.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))
    plt.tight_layout()
    plt.savefig(save_path)
    # plt.show()


def main():
    df = load_results_dataframe()
    plot_performance_graph(df, "docs/thesis_latex/images/performance_graph.png")


if __name__ == "__main__":
    main()
