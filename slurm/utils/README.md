# Utils

These scripts are auxiliary scripts to submit jobs to slurm. The idea is that
`../submit.sh` will call the function `f` of one of this file to submit the 
jobs.

The `./lib` contains bash files that are shared by multiples scripts

## Scripts

* *champsim_1core.sh*: Run single-thread champsim simulation.
* *champsim_ncore.sh*: Run N-thread champsim simulation.
