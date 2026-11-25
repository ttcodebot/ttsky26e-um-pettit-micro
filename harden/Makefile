# Harden tt_um_pettit_micro on this machine with LibreLane.
#
#   make harden TAG=t1 [OVERLAY=trial.json] [TO=OpenROAD.GlobalRouting]
#   make synth  TAG=s1          synthesis only: runs/s1/*-yosys-synthesis/reports/stat.rpt
#   make status RUN=runs/t1 ; make clean
#
# LibreLane and the tools come from the dev shell of a LibreLane checkout
# (LIBRELANE, 3.0 or newer for the PDN_* names), the PDK from PDK_ROOT.
# Results: runs/<tag>/final/.
LIBRELANE ?= $(HOME)/projects/tiny_tapeout/librelane
export PDK_ROOT ?= $(HOME)/projects/fossi
TAG ?= $(shell date +%Y%m%d-%H%M%S)
TO ?=
OVERLAY ?=
CONF = $(if $(OVERLAY),--overlay=$(OVERLAY),)
FLOW = librelane --pdk-root $(PDK_ROOT) --hide-progress-bar --run-tag $(TAG)

ifeq ($(IN_NIX_SHELL),)
NIX_RUN = nix-shell $(LIBRELANE)/shell.nix --run
else
NIX_RUN = sh -c
endif

harden:
	$(NIX_RUN) "python3 configure.py $(CONF) && $(FLOW) $(if $(TO),--to $(TO),) config_merged.json"

synth:
	$(NIX_RUN) "python3 configure.py $(CONF) && $(FLOW) --to Yosys.Synthesis config_merged.json"

RUN ?=
status:
	python3 status.py $(RUN)

clean:
	rm -rf runs config_merged.json

.PHONY: harden synth status clean
