import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import argparse
import json
import os
import pandas as pd

from teams import NFL

DATA_PATH = "dataset/raw_transcripts.json"
OUTPUT_DIR = "output/"
# One transcript in 1962 and then there is a 7 year gap with no game
# transcripts until 1969.
NO_PLOT_1962 = True
# DPI for the scatter plot
DPI = 300

def word_count(phrase):
    '''Return dictionaries of format year: (word count, number of games) for
    NFL, NCAA, and both NFL and NCAA football games.'''

    with open(DATA_PATH) as f:
        data = json.load(f)

    nfl = {}
    ncaa = {}
    all = {}

    def add_to_dict(items, yr, word_count):
        if yr not in items:
            items[yr] = [word_count, 1]
        else:
            items[yr][0] += word_count
            items[yr][1] += 1

    for items in data.values():
        yr = int(items['year'])
        transcript = items['transcript'].lower()
        word_count = transcript.count(phrase)

        if items['teams'][0] in NFL:
            add_to_dict(nfl, yr, word_count)
        else:
            add_to_dict(ncaa, yr, word_count)
        add_to_dict(all, yr, word_count)

    return nfl, ncaa, all


def plot(data:dict, title:str, results_path:str, min_sample_size:int):
    '''Plot average per-game word usage for every provided year having at
    least min_sample_size game transcripts.'''

    yrs = []
    per_game_avgs = []
    for yr, (total_word_count, n) in data.items():
        if NO_PLOT_1962 and yr == 1962:
            continue
        if n >= min_sample_size:
            yrs.append(yr)
            per_game_avgs.append(total_word_count / n)

    model_x = np.array(yrs).reshape(-1, 1)
    model = LinearRegression()
    model.fit(model_x, per_game_avgs)

    plt.clf()
    plt.scatter(yrs, per_game_avgs, color='green', marker='.', label="Year Average")
    plt.plot(yrs, model.predict(np.array(model_x)), color="red", label="Regression Line")
    plt.title(title)
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("Per-Game Average")
    plt.savefig(results_path, dpi=DPI)


def table_output(data:dict, results_path:str, nfl:bool, ncaa:bool):
    '''Write table to csv file detailing for each year in the data the
    total number of times the target phrase was said, the number of game
    transcripts, and the average phrase occurrence per game'''

    filename = "per_game_stats.csv"
    if nfl:
        filename = 'nfl_' + filename
    elif ncaa:
        filename = 'ncaa_' + filename

    for yr, (total_word_count, n) in data.items():
        data[yr] = (total_word_count, n, total_word_count / n)

    df = pd.DataFrame.from_dict(data)
    df.T.to_csv(results_path, header=["Total Phrase Count", "Game Transcripts", "Average Per Game Count"], index_label="Year")


def main():
    parser = argparse.ArgumentParser(description="Yearly trends of mentions of specific phrase in NFL and NCAA football broadcasts.")
    parser.add_argument("phrase", help="Phrase to run analysis for.")
    parser.add_argument("-sample", type=int, default=5, help="Minimum number of transcripts in a year to include in plot.")
    args = parser.parse_args()

    phrase = args.phrase.lower()

    directory = f"{OUTPUT_DIR}/{phrase}-n={args.sample}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    nfl, ncaa, both = word_count(phrase)

    phrase_upper = phrase[0].upper() + phrase[1:]
    title_end = f"\"{phrase_upper}\" Mentions Per Game"

    plot(nfl, f"NFL {title_end}", f"{directory}/nfl_plot.png", args.sample)
    table_output(nfl, f"{directory}/nfl_per_game_stats.csv", True, False)

    plot(ncaa, f"NCAA {title_end}", f"{directory}/ncaa_plot.png", args.sample)
    table_output(ncaa, f"{directory}/ncaa_per_game_stats.csv", False, True)

    plot(both, f"NFL and NCAA {title_end}", f"{directory}/plot.png", args.sample)
    table_output(both, f"{directory}/per_game_stats.csv", False, False)


if __name__ == "__main__":
    main()