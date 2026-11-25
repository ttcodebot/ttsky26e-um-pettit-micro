# Render frames of the demo to PNG:  make UI=0 T0=40 N=2 STEP=16
UI ?= 0
T0 ?= 40
N ?= 1
STEP ?= 16
all:
	iverilog -g2012 -o render.vvp render.v ../../src/tt_um_pettit_micro.v
	vvp -n render.vvp +UI=$(UI) +T0=$(T0) +N=$(N) +STEP=$(STEP)
	python3 ppm2png.py frame_$(UI)_*.ppm
clean:
	rm -f render.vvp frame_*.ppm frame_*.png
