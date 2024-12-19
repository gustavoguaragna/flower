"""Generate plots from json files."""

import json
import os
from typing import List, Tuple

import matplotlib.pyplot as plt

# Get the current working directory
DIR = os.path.dirname(os.path.abspath(__file__))


def read_from_results(path: str) -> Tuple[str, str, List[float], str, str]:
    """Load the json file with recorded configurations and results."""
    with open(path, "r", encoding="UTF-8") as fin:
        data = json.load(fin)
        algorithm = data["run_config"]["algorithm"]
        model = data["run_config"]["model-name"]
        accuracies = [res["accuracy"] * 100 for res in data["round_res"]]
        dataset = data["run_config"]["dataset-name"]
        num_classes = data["run_config"]["dataset-split-num-classes"]

        return algorithm, model, accuracies, dataset, num_classes


def make_plot(dir_path: str, plt_title: str) -> None:
    """Given a directory with json files, generated a plot using the provided title."""
    plt.figure()
    with os.scandir(dir_path) as files:
        for file in files:
            file_name = os.path.join(dir_path, file.name)
            print(file_name, flush=True)
            algo, m, acc, d, n = read_from_results(file_name)
            rounds = [i + 1 for i in range(len(acc))]
            print(f"Max accuracy ({algo}): {max(acc):.2f}")
            plt.plot(rounds, acc, label=f"{algo}-{d}-{n}classes")
    plt.xlabel("Rounds")
    plt.ylabel("Accuracy")
    plt.title(plt_title)
    plt.grid()
    plt.legend()
    plt.savefig(os.path.join(DIR, f"{plt_title}-{algo}"))


if __name__ == "__main__":
    # Plot results generated by the baseline.
    # Combine them into a full file path.
    res_dir = os.path.join(DIR, "../results/")
    title = "Federated Accuracy over Rounds"
    make_plot(res_dir, plt_title=title)
