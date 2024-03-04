# /* cSpell:disable */
import os
import json
import pandas as pd
from collections import defaultdict

# from matplotlib import pyplot as plt
# import matplotlib


def plot_robustness_graph(robustness_df, title, xlabel, ylabel, save_path):
    # sns.set_theme(style="whitegrid")
    # the df has the columns "company", "outcome", and "count"
    # make the barplot sideways
    # stack the bars with the same x value
    # # print(plt.style.available)
    # # plt.style.use("seaborn-v0_8-darkgrid")
    # set figure size
    # # robustness_df.plot(
    # #     kind="bar",
    # #     stacked=True,
    # #     color=["#2ca02c", "#ff7f0e", "#d62728"],
    # #     figsize=(10, 5),
    # # )
    # rotate plot 90 degrees
    # # plt.xticks(rotation=90)

    total_reports = (
        sum(robustness_df["success"])
        + sum(robustness_df["errors"])
        + sum(robustness_df["crashes"])
    )

    # # plt.title(title + f" (Total reports: {total_reports})")
    # # plt.xlabel(xlabel)
    # # plt.ylabel(ylabel)
    # move legend outside of plot
    # # plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))

    # make the y ticks integers
    # # plt.gca().yaxis.set_major_formatter(
    # # matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
    # # )

    # # plt.tight_layout()
    # # plt.savefig(save_path)
    # plt.show()

    # make 2 subplots, each containing half of the names
    # # robustness_df.iloc[: len(robustness_df) // 2].plot(
    # # kind="bar",
    # # stacked=True,
    # # color=["#2ca02c", "#ff7f0e", "#d62728"],
    # # figsize=(10, 5),
    # # )
    # # plt.xticks(rotation=90)
    # # plt.title(title + f" (Total reports: {total_reports})")
    # # plt.xlabel(xlabel)
    # # plt.ylabel(ylabel)
    # # plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
    # # plt.gca().yaxis.set_major_formatter(
    # # matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
    # # )
    # # plt.tight_layout()
    # # plt.savefig(save_path.replace(".png", "_1.png"))

    # # robustness_df.iloc[len(robustness_df) // 2 :].plot(
    # # kind="bar",
    # # stacked=True,
    # # color=["#2ca02c", "#ff7f0e", "#d62728"],
    # # figsize=(10, 5),
    # # )
    # # plt.xticks(rotation=90)
    # plt.title(title + f" (Total reports: {total_reports})")
    # # plt.xlabel(xlabel)
    # # plt.ylabel(ylabel)
    # # plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
    # # plt.gca().yaxis.set_major_formatter(
    # # matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
    # # )
    # # plt.tight_layout()
    # # plt.savefig(save_path.replace(".png", "_2.png"))
    # plt.show()


def load_results_dataframe():
    current_dir = os.path.dirname(__file__)
    results_path = os.path.join(current_dir, "robustness_results.json")
    results = json.load(open(results_path, "r"))
    crashes_per_cik = results["crashes_per_cik"]
    errors_per_cik = results["errors_per_cik"]
    success_per_cik = results["success_per_cik"]
    cik_to_name = results["cik_to_name"]

    total_reports = results["total_reports"]
    total_success = results["total_success"]
    total_errors = results["total_errors"]
    total_crashes = results["total_crashes"]

    print(f"Total reports: {total_reports}")
    print(f"Success rate: {total_success / total_reports * 100:.2f}%")
    print(f"Error rate: {total_errors / total_reports * 100:.2f}%")
    print(f"Crash rate: {total_crashes / total_reports * 100:.2f}%")

    # robustness_df = pd.DataFrame(columns=["company", "reports", "success", "errors", "crashes", "success rate"])
    robustness_dict = defaultdict(list)
    names = []
    ciks = list(cik_to_name.keys())
    # ciks = ciks[]

    for cik in ciks:
        # robustness_dict["company"].append(name)
        name = cik_to_name.get(cik, "Unknown")
        names.append(name)
        robustness_dict["success"].append(success_per_cik.get(cik, 0))
        robustness_dict["errors"].append(errors_per_cik.get(cik, 0))
        robustness_dict["crashes"].append(crashes_per_cik.get(cik, 0))

    robustness_df = pd.DataFrame(robustness_dict, index=names)
    return robustness_df


def main():
    robustness_df = load_results_dataframe()
    plot_robustness_graph(
        robustness_df,
        "Robustness of SEC data retrieval",
        "Company",
        "Number of reports",
        "docs/thesis_latex/images/robustness.png",
    )


if __name__ == "__main__":
    main()
