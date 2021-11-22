#!/bin/bash


filename="./scripts/pdede_trace_list.txt"
while read line; do
./run_champsim.sh hashed_perceptron-baseline-ipcp_isca-ipcp_isca-no-no-no-no-lru-lru-lru-srrip-drrip-lru-lru-lru-1core 10 10 /media/ashish/Windows/Ashish/traces/public $line  ./baseline &
done < $filename

