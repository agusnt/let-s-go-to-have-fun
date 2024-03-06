# Berti sensitivity heatmap

This folder include an script to produce a 7-way graph about the berti 
sensitivity to difference confidences. This 7-way (graphs) are the following:

1. L1D Accuracy
2. L2C Accuracy
3. L1D MPKI
4. L2C MPKI
5. L1D PFKI
6. L2C PFKI
7. Speedup

## Components

### run.sh

```Bash
#
# Generate the necessary data for a berti sensitivity heat-map. After it 
# generates a heat-map
#
# @param $1 : data from ChampSim it must include a no-prefetch data version and 
# the format of the files must be named as follow: L1D_$CONF_L2C_$CONF
#
```

### lib 

This folder contains all the extra resources that we need to generate the graph.
