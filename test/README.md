# Testbench

A [cocotb](https://docs.cocotb.org/en/stable/) bench that compares every clock of three frames of `uo_out` with a cycle-exact model (`model.py`) and measures the VGA timing from the sync pins. `render/` draws frames as PNG files.
See below to get started or for more information, check the [website](https://tinytapeout.com/hdl/testing/).

## How to run

To run the RTL simulation:

```sh
make -B
```

To run gatelevel simulation, first harden your project and copy `../runs/wokwi/results/final/verilog/gl/{your_module_name}.v` to `gate_level_netlist.v`.

Then run:

```sh
make -B GATES=yes
```

If you wish to save the waveform in VCD format instead of FST format, edit tb.v to use `$dumpfile("tb.vcd");` and then run:

```sh
make -B FST=
```

This will generate `tb.vcd` instead of `tb.fst`.

## How to view the waveform file

Using GTKWave

```sh
gtkwave tb.fst tb.gtkw
```

Using Surfer

```sh
surfer tb.fst
```
