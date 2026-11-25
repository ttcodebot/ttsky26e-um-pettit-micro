#!/usr/bin/env python3
"""configure.py [--overlay=FILE] - the LibreLane configuration for a local
harden, built the way tt-support-tools' create_user_config does it for a
micro tile: ../src/config.json, then the tile's die, floorplan template and
power grid (tech.py's Sky130Tech.micro_librelane_config, copied below), then
recipe.json (this project's own variables, each with a "//" saying why), then
the overlay (one trial's change), last wins.  Writes config_merged.json."""
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TILE_SIZES = {"micro": [0, 0, 70.38, 51.68], "1x1": [0, 0, 161.00, 111.52]}
# tt-support-tools tech.py, Sky130Tech.micro_librelane_config (53b9a09): the
# micro tile routes up to met3; its horizontal met3 stripes are its power
# pins, crossed by the container project's met4 stripes
MICRO = {
    "RT_MAX_LAYER": "met3",
    "PDN_MULTILAYER": True,
    "PDN_VERTICAL_LAYER": "met2",
    "PDN_VWIDTH": 0.8,
    "PDN_VSPACING": 0.58,
    "PDN_VPITCH": 61.18,
    "PDN_VOFFSET": 0.92,
    "PDN_HORIZONTAL_LAYER": "met3",
    "PDN_HWIDTH": 1.0,
    "PDN_HSPACING": 9.88,
    "PDN_HPITCH": 21.76,
    "PDN_HOFFSET": 6.8,
}


def load_json(path):
    with open(path, encoding="utf8") as f:
        return {k: v for k, v in json.load(f).items() if not k.startswith("//")}


def main():
    info = yaml.safe_load(open(os.path.join(ROOT, "info.yaml")))["project"]
    tiles = info["tiles"]
    cfg = load_json(os.path.join(ROOT, "src", "config.json"))
    # src/config.json's dir:: paths are relative to src/; config_merged.json lives here
    for k, v in cfg.items():
        if isinstance(v, str) and v.startswith("dir::"):
            cfg[k] = "dir::../src/" + v[5:]
    cfg.update({
        "DESIGN_NAME": info["top_module"],
        "VERILOG_FILES": ["dir::../src/" + s for s in info["source_files"]],
        "DIE_AREA": TILE_SIZES[tiles],
        "FP_DEF_TEMPLATE": "dir::tt_block_%s_pg.def" % tiles,
        "VDD_PIN": "VPWR",
        "GND_PIN": "VGND",
        "RT_MAX_LAYER": "met4",
    })
    if tiles == "micro":
        cfg.update(MICRO)
    recipe = os.path.join(HERE, "recipe.json")
    if os.path.exists(recipe):
        cfg.update(load_json(recipe))
    overlay = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--overlay=")), None)
    if overlay:
        cfg.update(load_json(overlay))
    # the tools drop the deprecated FP_PDN_<name> when they set PDN_<name>
    for k in [k for k in cfg if k.startswith("FP_PDN_") and k[3:] in cfg]:
        del cfg[k]
    # the template writes its booleans as 0 / 1
    BOOL_PREFIXES = ("RUN_", "ERROR_ON_", "LINTER_INCLUDE", "DESIGN_REPAIR_", "MAGIC_DEF", "MAGIC_WRITE")
    BOOL_KEYS = ("GRT_ALLOW_CONGESTION", "FP_PDN_MULTILAYER", "PDN_MULTILAYER")
    for k, v in list(cfg.items()):
        if type(v) is int and v in (0, 1) and (k.startswith(BOOL_PREFIXES) or k in BOOL_KEYS):
            cfg[k] = bool(v)
    out = os.path.join(HERE, "config_merged.json")
    with open(out, "w", encoding="utf8") as f:
        json.dump(cfg, f, indent=2)
    print("%s: %s tile %s%s" % (out, info["top_module"], tiles, ", overlay %s" % overlay if overlay else ""))


if __name__ == "__main__":
    main()
