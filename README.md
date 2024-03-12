#  Let's go to have fun

A bunch of script to make my life easier. This script solve or speed up my work
with ChampSim, generate figures...

I am currently changing the organization of this repo to a more useful one.
So breaking stuff is expected.

## Folder

* *db*: MongoDB docker files and README.
* *slurm*: Scripts to submit jobs to slurm.
* *ChampSim*: ChampSim scripts.
* *Figures*: Scripts to generate figures.
* *utils*: Script that are useful.

## Requirements

`Python3` and some libraries (like `numpy` or `matplotlib`). See the 
`requirements.txt` for more information.

My recommendation is using a [virtual environment](https://docs.python.org/3/library/venv.html)
and install all the dependencies with `pip install -r requirements.txt`

## TODO

* Define an official way to communicate `get_info.py` and the `parser.py`.
* Extend the key mt_lg_placeholder, so it can be multiples placeholders.
* Fix populate database with multicore, right now only can get the speedup
