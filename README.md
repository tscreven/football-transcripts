# Football Broadcast Transcript Analysis

Fill in rest of this later

## Data Download and Setup
The broadcast transcript dataset is sourced from Merullo et al.'s paper published in EMNLP [1].

Download the 1.4G dataset from: 
> https://drive.google.com/file/d/15XVD0kumvPhJkwj20an2kwWCdL9w_cy7/view?usp=sharing

Move the downloaded zip file to this project and unzip it. For example, on Macs:
```bash
cd football-transcripts
mv Downloads/dataset.zip .
unzip dataset.zip
rm -f dataset.zip
```

The downloaded zip file should have the name `dataset.zip` so when it is expanded it will be saved to a directory titled `dataset`. The code assumes the dataset is in folder `dataset/`. If you want to rename the directory, change the value of variable `OUTPUT` in [analyze.py](./analyze.py).

The only file needed from the dataset is `raw_transcripts.json` so feel free to
delete the rest of the files to save disk space.

### References
[1] Merullo, J., et al. (2019). "Climate Dynamics." *Empirical Methods in Natural Language Processing*. https://doi.org/10.18653/v1/D19-1666