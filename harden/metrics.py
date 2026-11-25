#!/usr/bin/env python3
"""metrics.py RUN... - the numbers that decide a run, one column per run."""
import json, os, re, sys, collections

KEYS = [("synth um2", None), ("stdcell um2", "design__instance__area__stdcell"), ("util", "design__instance__utilization"),
        ("clock buf um2", "design__instance__area__class:clock_buffer"), ("repair buf um2", "design__instance__area__class:timing_repair_buffer"),
        ("fill um2", "design__instance__area__class:fill_cell"), ("wire um", "route__wirelength"),
        ("route DRC", "route__drc_errors"), ("magic DRC", "magic__drc_error__count"), ("LVS", "design__lvs_error__count"),
        ("antenna", "route__antenna_violation__count"), ("slew viol", "design__max_slew_violation__count"),
        ("hold ws", "timing__hold__ws"), ("setup ws", "timing__setup__ws")]
rows = collections.defaultdict(list)
for run in sys.argv[1:]:
    try:
        m = json.load(open(os.path.join(run, "final", "metrics.json")))
    except OSError:
        m = {}
    area = "-"
    for d in sorted(os.listdir(run)):
        f = os.path.join(run, d, "reports", "stat.rpt")
        if d.endswith("yosys-synthesis") and os.path.exists(f):
            area = re.search(r"Chip area for module.*: ([\d.]+)", open(f).read()).group(1)
    trail = [m[k] for k in sorted((k for k in m if k.startswith("route__drc_errors__iter:")), key=lambda k: int(k.split(":")[1]))]
    for name, key in KEYS:
        v = area if key is None else m.get(key, "-")
        rows[name].append("%.3f" % v if isinstance(v, float) and abs(v) < 100 else ("%.0f" % float(v) if v != "-" else v))
    rows["router trail"].append(" ".join(str(t) for t in trail) or "-")
print("%-16s" % "" + "".join("%-22s" % os.path.basename(r.rstrip("/")) for r in sys.argv[1:]))
for name, vals in rows.items():
    print("%-16s" % name + "".join("%-22s" % v for v in vals))
