# ChampSim

A bunch of for ChampSim

## Folders

* `config_json`: json files with different configurations.
* `lib`: common script files.
* `mixes`: generate mixes for multicore simulations.
* `no_db`: scripts that does not use the db.
* `utils`: a bunch of useful scripts.

## Scripts

### pop_db.py

Populate a mongoDB database with a folder of ChampSim outputs. 
[Check this section](##-DB-JSON)

### get_info.py

```
Parse ChampSim outputs to csv

Enviromental Vars:
    OLD_CHAMPSIM if has value it means tha you are using and older version of
    champsim, and some of the stats maybe will not work

Arguments:
  @1 -> directory to parse
  @2 -> What to get from this information, see options in comment below

@Author: Navarro-Torres, Agustin 
@Email: agusnt@unizar.es, agusnavarro11@gmail.com

Options to get information:
  - speedup: speedup of all benchmarks
       @3 -> Base elements
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - mpki: demand mpki X cache level
       @3 -> level of cache
       @4 -> event for mpki (LOAD) with underline
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - apki: demand apki X cache level
       @3 -> level of cache
       @4 -> event for mpki (LOAD) with underline
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - hpki: demand hpki X cache level
       @3 -> level of cache
       @4 -> event for mpki (LOAD) with underline
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - pfki: prefetch per kilo instruction
       @3 -> level of cache
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - queues: full every one thousand access for queues
       @3 -> queue type (RQ, WQ, PQ, PTWQ) 
       @4 -> level of cache
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - accuracy: prefetch accuracy X cache level
       @3 -> level of cache
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - accuracy_late: prefetch accuracy including late X cache level
       @3 -> level of cache
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - latency: get average latency
       @3 -> level of cache
       @4 -> Y for memory intensive, N for normal
       @5 -> Memory intensive base
  - branch_accuracy: get branch accuracy
       @3 -> Y for memory intensive, N for normal
       @4 -> Memory intensive base
  - branch_mpki: get branch MPKI 
       @3 -> Y for memory intensive, N for normal
       @4 -> Memory intensive base
  - branch_mpki: get average ROB occupancy at branch miss prediction
       @3 -> Y for memory intensive, N for normal
       @4 -> Memory intensive base
  - energy: get energy values (miliJules)
       @3 -> memory levels, separated by _ (e.g.: L1D_L2C_LLC_DRAM)
       @4 -> energy file
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - rel_energy: get relative energy
       @3 -> memory levels, separated by _ (e.g.: L1D_L2C_LLC_DRAM)
       @4 -> energy file
       @5 -> Y for memory intensive, N for normal
       @6 -> Memory intensive base
  - db: add everything into the database
       @3 -> JSON with the information
```

## DB JSON

The JSON db has to have the following information

```json
{
    "connect": "mongodb://user:pass@localhost:27017/ # how to connect",
    "db": "#database name",
    "collection": "#collection name",
    "base": "# base for speedup",
    "base_llc": "# base for memory intensive (LLC MPKI > 1); optional",
    "multicore": # bool; set to true if you whn to populate with multicore simulations,
    "base_energy": # base for energy, only work if using used with energy; optional
    "energy": # path to the energy file (example in config_json/energy.json); optional
}
```
