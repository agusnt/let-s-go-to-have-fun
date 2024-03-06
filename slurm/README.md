# Slurm

A set of script to run jobs using `slurm`.

The main script `submit.sh` can be run using the following arguments:

```bash
# Submit jobs into slurm
#
# Parameters:
#   $1 : Bin folder
#   $2 : Memory intensive files
#   $3 : Utils to load
#   $4 : Output folder
#   $5- : Extra arguments for the utils
#
```

You have to define a `.env` with the following vars: 
* `OUT`: output folder.
* `MAIN_TRACES`: folder to where the traces are.

## Folders

* *lists*: folder with the different list to filter the traces or applications
to run.
* *utils*: a bunch of scripts that contains the scripts for submitting the 
jobs into slurm.
