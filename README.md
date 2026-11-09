# Football Broadcast Transcript Analysis

This codebase analyzes the long term trends of the frequency phrases are said
in both NFL and college football broadcasts. Specifically, it analyzes over the
years how often a phrase is said. 

The main Python script `analyze.py` generates a scatter plot and a table for a
given target phrase. The scatter plot displays the yearly per-game broadcast
average a provided target phrase is said. It also displays a regression line
demonstrating the linear trend. The table is written to a CSV file and details
for each year the total number of times the target phrase is said, the number
of game broadcasts in the dataset for that year, and the per-game broadcast
target phrase average.

## Outline
1. [Dataset Download](#dataset-download)
2. [Environment Setup](#environment-setup)
3. [Usage](#usage)
4. [Example Usage](#example-usage)

## Dataset Download
The broadcast transcript dataset is sourced from Merullo et al. [1]. It
contains both NFL and college (NCAA) football broadcast transcripts between
1962 and 2018; dataset size information [here](./dataset_size.csv).

Download the 1.4G dataset from: 
> https://drive.google.com/file/d/15XVD0kumvPhJkwj20an2kwWCdL9w_cy7/view?usp=sharing

Clone the repository, then move the downloaded zip file to this project, and
then expand the zip file. For example, on computers running MacOS:

```bash
git clone https://github.com/tscreven/football-transcripts.git
cd football-transcripts
mv Downloads/dataset.zip .
unzip dataset.zip
rm -f dataset.zip
```

The downloaded zip file should have the name `dataset.zip` so when it is
expanded it will be saved to a directory titled `dataset`. The code assumes the
dataset is in folder `dataset/`. If you want to rename the directory, change
the value of variable `DATA_PATH` in [analyze.py](./analyze.py).

The only file needed from the dataset is `raw_transcripts.json` (136M).

## Environment Setup
Minimum required Python version is 3.10. Run the following command to install
third-party packages used in Python analysis.
```bash
pip install -r requirements.txt
```

## Usage
File `analyze.py` runs the analysis described above. It generates analysis for
three sets of broadcasts. 
1. NFL broadcasts only
2. College football broadcasts only
3. The entire dataset: both NFL and college football broadcasts

Each subset has its own CSV file and scatter plot image; each execution
creates 6 files. 

```
python3 analyze.py phrase -sample n
```
* `phrase`: Positional argument to input the target phrase. Phrase is not
  case sensitive; the code automatically lowercases all processed transcripts
  and the provided phrase. No backslash (\\) character is necessary for spaces
  in the phrase, the code processes spaces.
* `-sample`: Optional integer argument setting `n` as the minimum number of
  broadcast transcripts for years plotted on the scatter plot.  Default
  value is 5. This argument has no effect on the table written to the CSV file.
  If given, must be written after `phrase`.

Execution results are written to directory `output/<phrase>-n=<sample>/`.

The code defaults to not plot the one broadcast transcript in 1962 because
there is a seven year gap between it and the next year with a broadcast (see
[dataset_size.csv](./dataset_size.csv)). To avoid the large gap in the plot, it
defaults to not show it. To change this, set variable `PLOT_1962` to `True`
in [analyze.py](./analyze.py). Also, if `-sample` is set to a number larger
than 1, this point will not be plotted no matter the value of `PLOT_1962`. 

### Example Usage
For example, if you want to see how awareness of concussions on football
broadcasts has changed over the years, you can run the following command:

```bash
python3 analyze.py concussion -sample 10
```

This creates three CSV files and three scatter plot images. Below is the NFL
and college football combined broadcast scatter plot.

![](./example_output/plot.png)

See directory [example_output/](./example_output/) to examine all six files.


## References
[1] Merullo, J., et al. (2019). "Investigating Sports Commentator Bias within a
Large Corpus of American Football Broadcasts." *Empirical Methods in Natural
Language Processing*. https://doi.org/10.18653/v1/D19-1666