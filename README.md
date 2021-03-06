# BTB_Organization
This is Computer Architechture course project.
Here we're implementing a Branch-Target-Buffer given in Pdede research paper. Pdede stands for Partition, Deduplication, and Decoding these are the three main idea presented in the paper also the implementaion for that is here.

Presentation Link:
https://youtu.be/lAzgtaEaW68

Slides Link:
https://docs.google.com/presentation/d/1i_Kw-M8OrToxMtKQowiJLcrr_9xy2GO1gi885BS0odM/edit?usp=sharing

<p align="center">
  <p> This repository contains extension to ChampSim including a two-level Branch Target Buffer (BTB), a five-level Page Table Walker (PTW) (backed by four MMU Caches) and Virtually Indexed, Physically Tagged (VIPT) level 1 caches. <p>
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

# Replicating the Results
The binaries with various configuration are provided in `bin/`. you can use them or you can build your own.
We first build the binary with baseline BTB with L1BTB_SET = 32 and L1BTB_WAY = 2. you can set these values in `inc/baseline_btb.h`. 
Now the total size(in KB) of this L1 baseline BTB can be calculated as:
```
NUM_SET*NUM_WAY*(TAG_SIZE+ VALID_BIT_SIZE+ TARGET_SIZE + LRU)
for our default baseline configuration we get-
32*2*(56+1+64+1) = 7808 = ~1KB
```

Now we'll build binary with pdede BTB with configurations as follows:-
L1BTB_SET = 64
L1BTB_WAY = 2
NUM_REGION = 2, NUM_PAGE = 8
set these values in `inc/pdede.h`

Total size(in KB) of this L1 PDEDE BTB can be calculated as:
```
NUM_SET*NUM_WAY*(TAG_BIT+ VALID_BIT+ (REGION_PTR+PAGE_PTR+OFFSET) + LRU) + NUM_REGION*(REGION_BIT+LRU) + NUM_PAGE*(PAGE_BIT+LRU)

64*2*(56+1+ (1+3+19)+1) + 2*(29+3)+ 8*(16+3) = ~1.2KB (Actual storage requirement will be lesser because here while calculating we did not consider target encoding part which depends on percentage of branches sharing the same page).
```


# Results

The traces used in evalution can be found in `scripts/pdede_trace_list.txt`. For each trace, the results are captured for 10M instructions after a warmup of 10M instructions. The results for PDEDE BTB designs can be found in `pdede_128s_4r_16p_res_10M` and `pdede_64s_2r_8p_res_10M`. Also the results for Baseline BTB having size comparable to PDEDE BTB can be found in `baseline_32s_2w_10M` and `baseline_64s_2w_10M`.

# Division Of Labor

Ashish (180050013) : Implementation, Github readme, Presentation.
  
Sudhir (170050053) : Testing and Plotting, Animation.



