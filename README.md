# ls4_sim
:telescope: Scheduling library for LS4.

Implements the Integer Linear Programming scheduling algorithm described in 
[Bellm et al. 2019](https://dx.doi.org/10.1088/1538-3873/ab0c2a) (PASP 131, 1000).

## Installation

You will need a license for the [Gurobi](http://www.gurobi.com/) optimizer on the machine you want to run simulations on.  [Free academic licenses](http://www.gurobi.com/academia/for-universities) are readily available.

You are strongly encouraged to use `conda` and a conda environment for the installation.

The Python import path remains `ztf_sim` for compatibility, while the new command-line entry points are `run_ls4_sim`, `analyze_ls4_sim`, and `load_ls4_sim`.


```
conda create -n ls4_sim_test

conda activate ls4_sim_test

conda install python=3.11


conda config --add channels conda-forge 
conda config --add channels http://conda.anaconda.org/gurobi
conda install pip numpy scipy astropy astroplan pandas scikit-learn xgboost sqlalchemy gurobi

pip install transitions

pip install -e .
```

(To remove the environment, use `conda remove --name ls4_sim_test --all`.)


## Configuration

### Scheduler Configuration

The scheduler configuration determines which observing programs will run (fields, filters, cadences, etc.)  

An example set of scheduler configuration files is provided in `sims/`.

### Simulation Configuration

The simulation configuration determines which nights to simulate, which historical weather to use, and whether to overwrite the existing simulated database.

An example configuration file is provided in `config/default.cfg`.

## Running

`run_ls4_sim --help` summarizes the argument of the command line driver for the simulations.  Assuming you've copied the configuration files to your current directory, you should now be able to run

```
run_ls4_sim example_scheduler_config.json default.cfg
```

which will write an sqlite database file named `example_ls4_schedule.db` to the current directory.

## Output

The simulated schedule is written to a SQLite database in the LSST [Operations Simulator format](https://www.lsst.org/scientists/simulations/opsim/summary-table-column-descriptions-v335) with a few additional columns.  Example code for reading and summarizing the simulated schedule is located in the `bin/` directory, and can be run as

```
analyze_ls4_sim example_ls4_schedule.db
```

The simulator also writes a logfile, which may be monitored while the simulation is running with `tail -f example_ls4_schedule_log.txt`

For quick-look plots, run:

```
plot_ls4_sim example_ls4_schedule.db
```

This writes sky, nightly-count, and filter-usage PNGs in the current directory.
