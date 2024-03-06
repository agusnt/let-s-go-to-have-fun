# List

A set of list with the applications/traces that must be submitting to slurm.
You can use this list to filter the jobs to reduce your simulation time.

Every file is a script with a bash list named `TRACE_INT` that contains the
applications/traces that will be **SUBMITTED**.

## Lists

* *no_list.sh*: run all applications/traces.
* *alderlake_no_pf_mem_int.sh*: ChampSim traces that their LLC MPKI is higher than
1 in an Alderlake CPU without hardware prefetching.

