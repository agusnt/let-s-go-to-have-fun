# Bash

A set of bash scripts to parse the ChampSim outputs into CSV or 
human readable format.

The lib directory contains auxiliary bash functions.

Before using this scripts you must set the vars in `../lib/set_var.sh`

## Scripts

### accuracy.sh

```Bash
#
# Get prefetch accuracy (Memory Intensive Traces)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> cache level (L1I, L1D, L2C, LLC, DTLB, STLB)
#   $3 -> Y if count lates prefetch 
#
```

### latency.sh

```Bash
#
# Get average miss latency (Memory Intensive)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> Cache level (L1I, L1D, L2C, LLC, DTLB, STLB)
#
```

### mpki.sh

```Bash
#
# Get demand cache MPKI (Memory Intensive traces)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> cache level: (L1I, L1D, L2C, LLC, DTLB, STLB)
#   $3 -> mpki, apki, hpki
#
```

### queues.sh

```Bash
#
# Get queues info (speedup memory intensive)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> cache level (L1I, L1D, L2C, LLC, DTLB, STLB)
#   $3 -> RQ, WQ, PQ, PTWQ
#
```

### speedup.sh

```Bash
#
# Get SpeedUp (Memory Intensive)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#
```

### best.sh

```Bash
#!/bin/bash
#
# Get the best speedup (Memory Intensive Traces)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#
```

### branch_accuracy.sh

```Bash
#!/bin/bash
#
# Get branch accuracy (Memory Intensive Traces)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#
```

### branch_mpki.sh

```Bash
#!/bin/bash
#
# Get branch MPKI (Memory Intensive Traces)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#
```
### branch_rob.sh

```Bash
#!/bin/bash
#
# Get average ROB occupancy at branch miss prediction (Memory Intensive Traces)
#
# Parameters:
#   $1 -> directory with the simulation outputs
#
```

### energy.sh

```Bash
#!/bin/bash
#
# Get energy (Memory Intensive Traces)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> Energy levels, e.g: L1D L2C LLC DRAM
#
```

### rel_energy.sh

```Bash
#!/bin/bash
#
# Get relative energy (Memory Intensive Traces)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> Energy levels, e.g: L1D L2C LLC DRAM
#
```

### rel_energy.sh

```Bash
#!/bin/bash
#
# Get relative energy (Memory Intensive Traces)
#
# Author: Navarro Torres, Agustín
# Email: agusnavarro11@unizar.es, agusnt@unizar.es
#
# Parameters:
#   $1 -> directory with the simulation outputs
#   $2 -> Energy levels, e.g: L1D L2C LLC DRAM
#
```

### common.sh

```
# Common configuration used for all the others scripts
```

## Requirements

A Unix-like system and its tools (`awk`, `grep`, `python3` ...)
