# Harden log

Local LibreLane 3.0.2 runs (`harden/`, sky130A open_pdks 8afc834) of tt_um_pettit_micro on the
micro tile. One paragraph per run; the recipe is `src/config.json`.

## The tile

Die 70.38 x 51.68 um, core 64.86 x 46.24 = 2999 um2 (141 sites x 17 rows), of which taps and
row ends take 175. Pins on the right edge on met3; routing on met1 to met3; power on met2
(two stripe pairs at the core's ends) and met3 (horizontal stripes, the tile's power pins, which
the container's met4 stripes cross). No via3 or met4 in the tile (precheck).

With the PDK's default synthesis cell list (no drive-strength-1 cells) a dfxtp_2 is 21.3 um2:
80 flops are 57% of the core by themselves. With the _1 cells allowed (`src/no_synth.cells`)
a design of about 2200 um2 synthesized, 39 flops and 220 gates here, routes clean.

## Runs (2026-11-25)

| run | RTL | synth um2 | change | result |
|-----|-----|-----------|--------|--------|
| t1 | first: 2 patterns, mask, 2 palettes, slow | 2993 | template config | global placement: utilization 121% |
| t2 | same | 2332 | _1 cells allowed, density 88 | detailed placement failed |
| t3 | no palette / slow options, stippled mask | 1979 | density 80 | clean, 83% utilization, router 8 iterations; 32 hold delay cells (325 um2), five clkbuf_16 (125) |
| t4 | 8 scenes (4 ops x mask), auto stepping | 2223 | density 88, one CTS cluster, clkbuf_2 / _4 | clean, 90%, router 30 iterations; 16 hold cells + 15 clkdlybuf as plain buffers |
| t5 | same | 2223 | t4 + hold margin 0.04 / 0.03 | clean, 85%, router 8 iterations |
| t6 | same | 2223 | t5 + clkdlybuf4s25_1 excluded | clean, no gain over t5 (6 um2): not kept |
| rc1 | same | 2223 | t5's settings in src/config.json, no overlay | identical to t5 |

rc1: standard cells 2542 um2 (84.8%), clock buffers 75, repair buffers 181, wire 5857 um; route
DRC, Magic DRC, LVS and antenna 0; setup +23.8 ns at max_ss against the 39 ns period; hold
+0.069 ns at min_ff (+0.25 at tt), on top of LibreLane's 0.25 ns clock uncertainty; 12 max-slew
warnings at the ss corner only. Gate-level simulation of rc1's netlist: three frames, 1,261,600
clocks, 0 mismatches. tt-support-tools precheck (main, 2026-11-25, micro rules): all checks pass.

Not promoted: `gds/` is not in the repository; the GitHub gds action builds its own.
