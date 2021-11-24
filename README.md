# BTB_Organization
This is Computer Architechture course project.
Here we're implementing a Branch-Target-Buffer given in Pdede research paper.

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

<p align="center">
  <h1 align="center"> ChampSim </h1>
  <p> ChampSim is a trace-based simulator for a microarchitecture study. You can find more information about ChampSim here (https://github.com/ChampSim/ChampSim). This repository contains extension to ChampSim including a two-level Branch Target Buffer (BTB), a five-level Page Table Walker (PTW) (backed by four MMU Caches) and Virtually Indexed, Physically Tagged (VIPT) level 1 caches. <p>
  <p> This repository contains implementation for state-of-the-art BTB designs including Shotgun, SN4L+Dis+BTB, FDIPX and Skewed BTB. This Repository also contains the implementation of PDede: Partitioned, Deduplicated, Delta Branch Target Buffer that is presented in the research paper attached in the repository. You can find more information about PDEDE in the paper.
</p>

# Requirements 

This setup is tested with GCC 7.5 and Ubuntu 18.04. To install GCC 7.5 in Ubuntu 20.04 :-

```
sudo apt install build-essential
sudo apt install g++-7
```

# Compile

Use build.sh script to compile different BTB and L1I prefetcher. Different BTB designs can be enabled using macros in `inc/champsim.h`. Here are the combinations for building different BTB designs :-

|BTB Desgin|Enable Macro|Default Size|L1I Prefetcher|
|----------|------------|------------|--------------|
|PDEDE|PDEDEBTB|128-entry(2-way) 4 region 16 pages|fdip|
|Baseline|BASELINE_BTB|8K-entry BTB (4-way)|fdip|



PDEDE_BTB configurations in `inc/pdede.h`
Inside the file we can play around with various parameter.

|Configuration|L1BTB_SET|L1BTB_WAY|NUM_REGION|NUM_PAGE|REGION_BIT|PAGE_BIT|OFFSET_BIT|
|-------------|---------|---------|----------|--------|----------|--------|----------|
|Default|128|2|4|16|29|16|19|


```
$ ./build.sh fdip

$ ./build.sh {L1I_PREFETCHER}
```

The Complete details of implementation is in `src/pdede.cc`.
Along with these other files where we made changes are-
`inc/block.h`
`src/main.cc`
`src/ooo_cpu.cc`


# Download server traces



You can download the server traces from here (https://drive.google.com/file/d/1qs8t8-YWc7lLoYbjbH_d3lf1xdoYBznf/view?usp=sharing).

# Run simulation

Execute `run_champsim.sh` with proper input arguments. <br>

```
Usage: ./run_champsim.sh [BINARY] [N_WARM] [N_SIM] [TRACE_DIR] [TRACE] [OUTPUT_DIR]
$ ./run_champsim.sh hashed_perceptron-baseline-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core 10 10 ../traces client_001.champsimtrace.xz ./baseline

${BINARY}: ChampSim binary compiled by "build_champsim.sh" (bimodal-no-no-lru-1core)
${N_WARM}: number of instructions for warmup (1 million)
${N_SIM}:  number of instructinos for detailed simulation (10 million)
${TRACE_DIR}: Directory containing traces.
${TRACE}: trace name (400.perlbench-41B.champsimtrace.xz)
${OUTPUT_DIR}: Directory containing results file.
```

# Replicating the results from the paper

The traces used in evalution can be found in `scripts/iccd_trace_list.txt`. For each trace, the results are captured for 50M instructions after a warmup of 50M instructions. The results for all the state-of-the-art BTB designs can be found in `iccd_sota_50M`. The scripts for generating plots can be found in `iccd_plots`.


