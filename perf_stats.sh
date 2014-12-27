#!/bin/sh

perf stat -a -e dTLB-load-misses -e dTLB-loads -e L1-dcache-loads \
    -e L1-dcache-load-misses -e L1-dcache-prefetch-misses sleep 1000

# perf stat -a  -e LLC-load-misses -e LLC-loads  sleep 1000

# perf stat  -a -e LLC-prefetch-misses -e LLC-prefetches sleep 1000
