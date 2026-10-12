#!/usr/bin/env python3
"""Dependency-free benchmark driver, live console charts and offline report."""
import argparse
import csv
import html
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import time

NAMES = {1: "Sort All", 2: "Sort K", 3: "Min Heap", 4: "Quick Select"}
COLORS = {1: "#fb7185", 2: "#fbbf24", 3: "#38bdf8", 4: "#a78bfa"}
DISTRIBUTIONS = ("random", "ascending", "descending", "duplicates")
SEED = 2026


def measure(binary, algorithm, n, k, distribution, repeats):
    result = subprocess.run(
        [str(binary), str(algorithm), str(n), str(k), str(SEED), distribution, str(repeats)],
        capture_output=True, text=True, timeout=90,
    )
    if result.returncode:
        raise RuntimeError(f"{NAMES[algorithm]} N={n} K={k} {distribution}: {result.stderr}")
    return json.loads(result.stdout)


def check(binary):
    count = 0
    for n in (1, 2, 9, 10, 11, 12, 31, 100):
        for k in sorted({1, max(1, n // 2), n}):
            for distribution in DISTRIBUTIONS:
                for algorithm in NAMES:
                    measure(binary, algorithm, n, k, distribution, 1)
                    count += 1
    print(f"PASS: {count} correctness cases, all compared with a fully sorted reference.", flush=True)


def chart(rows, title):
    maximum = max((row["median_ms"] for row in rows), default=1) or 1
    height = 86 + len(rows) * 48
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 {height}" role="img" aria-label="{html.escape(title)}">',
             '<rect width="100%" height="100%" rx="16" fill="#111b2e"/>',
             f'<text x="24" y="34" fill="#e2e8f0" font-size="18" font-family="sans-serif">{html.escape(title)}</text>']
    for i, row in enumerate(rows):
        y = 64 + i * 48
        width = max(2, row["median_ms"] / maximum * 530)
        parts.extend([
            f'<text x="24" y="{y+18}" fill="#cbd5e1" font-size="15" font-family="sans-serif">{row["algorithm"]}</text>',
            f'<rect x="165" y="{y}" width="{width:.2f}" height="26" rx="5" fill="{COLORS[row["id"]]}"/>',
            f'<text x="715" y="{y+18}" fill="#e2e8f0" font-size="14" font-family="monospace">{row["median_ms"]:.3f} ms</text>',
        ])
    parts.append(f'<text x="24" y="{height-14}" fill="#94a3b8" font-size="12" font-family="sans-serif">Median duration · lower is faster · linear scale</text></svg>')
    return "".join(parts)


def save_report(output, rows, metadata, status):
    output.mkdir(parents=True, exist_ok=True)
    (output / "results.json").write_text(json.dumps({"metadata": metadata, "status": status, "results": rows}, indent=2))
    fields = ("algorithm", "n", "k", "distribution", "median_ms", "min_ms", "max_ms", "verified")
    with (output / "results.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    summary = ["## ⚡ Algorithm performance", f"**{status}** · {len(rows)} measurements · {metadata['repeats']} repetitions + one warmup", "",
               "Times include input parsing, allocation, selection and captured output; exclude process startup and dataset generation. All results are checked against a sorted reference. Shared runner timings can vary between runs.", "",
               "| Input | K | Distribution | Algorithm | Median (ms) | Range (ms) | vs fastest |", "|---:|---:|---|---|---:|---:|---:|"]
    groups = {}
    for row in rows:
        key = (row["n"], row["k"], row["distribution"])
        groups.setdefault(key, []).append(row)
    panels = []
    for index, ((n, k, distribution), group) in enumerate(groups.items()):
        fastest = min(r["median_ms"] for r in group) or 1e-9
        for row in group:
            summary.append(f"| {n:,} | {k:,} | {distribution} | {row['algorithm']} | {row['median_ms']:.3f} | {row['min_ms']:.3f}–{row['max_ms']:.3f} | {row['median_ms']/fastest:.1f}× |")
        title = f"{distribution.title()} · N = {n:,} · K = {k:,}"
        svg = chart(group, title)
        (output / f"chart-{index+1:02d}.svg").write_text(svg)
        panels.append(f'<article data-distribution="{distribution}" data-size="{n}">{svg}</article>')
    summary.extend(["", "Download the **algorithm-performance** artifact for the interactive report, SVG charts, CSV and individual timing samples."])
    markdown = "\n".join(summary) + "\n"
    (output / "summary.md").write_text(markdown)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        Path(os.environ["GITHUB_STEP_SUMMARY"]).write_text(markdown)
    fastest_count = {}
    for group in groups.values():
        if len(group) == 4:
            winner = min(group, key=lambda r: r["median_ms"])["algorithm"]
            fastest_count[winner] = fastest_count.get(winner, 0) + 1
    leader = max(fastest_count, key=fastest_count.get) if fastest_count else "Pending"
    options = ''.join(f'<option value="{n}">{n:,} elements</option>' for n in sorted({r['n'] for r in rows}))
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kth Largest · Performance Lab</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#080e1b;color:#e2e8f0;font:16px/1.6 system-ui,sans-serif}
main{max-width:1120px;margin:auto;padding:48px 24px}.eyebrow{color:#38bdf8;letter-spacing:.18em;font-size:12px;font-weight:700}
h1{font-size:clamp(32px,5vw,56px);letter-spacing:-.04em;line-height:1.1;margin:18px 0}p{color:#94a3b8;max-width:850px}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin:32px 0}.metric{border:1px solid #26324a;border-radius:16px;padding:20px;background:#111b2e}.metric strong{display:block;font-size:26px;color:#f8fafc}.metric span{color:#94a3b8;font-size:13px}
.controls{display:flex;gap:18px;flex-wrap:wrap;margin:28px 0}select{background:#111b2e;color:#e2e8f0;padding:10px;border:1px solid #334155;border-radius:8px}label{display:flex;align-items:center;gap:10px}
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,450px),1fr));gap:18px}svg{width:100%;display:block}article[hidden]{display:none}a{color:#38bdf8}.legend{display:flex;gap:20px;flex-wrap:wrap;font-size:14px}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px}footer{margin-top:36px;color:#94a3b8;font-size:13px}
</style><main><div class="eyebrow">KTH LARGEST / PERFORMANCE LAB</div><h1>Four algorithms.<br>One fair comparison.</h1>
<p>Measured on identical, seeded datasets. Each result is verified against a sorted reference. Explore how input size, order and K change the cost of selection.</p>
'''
    page += f'<div class="metrics"><div class="metric"><strong>{html.escape(status)}</strong><span>Run status</span></div><div class="metric"><strong>{len(rows)}</strong><span>Verified measurements</span></div><div class="metric"><strong>{metadata["repeats"]}</strong><span>Samples per measurement</span></div><div class="metric"><strong>{leader}</strong><span>Most scenario wins</span></div></div>'
    page += '<div class="legend">' + ''.join(f'<span><i class="dot" style="background:{COLORS[i]}"></i>{name}</span>' for i, name in NAMES.items()) + '</div>'
    page += '<div class="controls"><label>Input size <select id="size"><option value="all">All sizes</option>' + options + '</select></label><label>Distribution <select id="distribution"><option value="all">All distributions</option>' + ''.join(f'<option>{d}</option>' for d in DISTRIBUTIONS) + '</select></label></div>'
    page += '<div class="charts">' + ''.join(panels) + '</div>'
    page += f'<footer>Median milliseconds; lower is faster. Bars use a separate linear scale per chart. Timing includes input parsing, allocation, selection and captured output. Dataset generation, reference sorting and process startup are excluded. Shared runner noise means small differences may not be significant.<br>Seed {SEED} · {html.escape(metadata["platform"])} · Commit {html.escape(metadata["commit"])}<br><a href="results.csv">Download CSV</a> · <a href="results.json">Raw samples &amp; metadata</a></footer></main>'
    page += '''<script>const size=document.querySelector('#size'),distribution=document.querySelector('#distribution');function filter(){document.querySelectorAll('article').forEach(p=>p.hidden=(size.value!=='all'&&p.dataset.size!==size.value)||(distribution.value!=='all'&&p.dataset.distribution!==distribution.value))}size.addEventListener('change',filter);distribution.addEventListener('change',filter);</script></html>'''
    (output / "index.html").write_text(page)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("benchmark-results"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    binary = args.binary.resolve()
    if args.check:
        check(binary)
        return
    sizes = sorted(set(int(n) for n in os.getenv("BENCHMARK_SIZES", "1000,5000,20000").split(",")))
    repeats = int(os.getenv("BENCHMARK_REPEATS", "5"))
    if not sizes or len(sizes) > 6 or not all(1 <= n <= 50000 for n in sizes) or not 1 <= repeats <= 20:
        parser.error("Use 1–6 input sizes between 1 and 50000, and 1–20 repetitions.")
    metadata = {"seed": SEED, "repeats": repeats, "platform": platform.platform(),
                "commit": os.getenv("GITHUB_SHA", "local"), "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "timing": "steady_clock, milliseconds; select() including stream parsing and captured output"}
    rows = []
    total = sum(len({max(1, n // 100), max(1, n // 2)}) for n in sizes) * 16
    status = "Complete"
    try:
        for n in sizes:
            for k in sorted({max(1, n // 100), max(1, n // 2)}):
                for distribution in DISTRIBUTIONS:
                    group = []
                    print(f"\n▶ {distribution.upper()}  N={n:,}  K={k:,}", flush=True)
                    for algorithm, name in NAMES.items():
                        result = measure(binary, algorithm, n, k, distribution, repeats)
                        samples = result["samples_ms"]
                        row = {"id": algorithm, "algorithm": name, "n": n, "k": k, "distribution": distribution,
                               "median_ms": statistics.median(samples), "min_ms": min(samples), "max_ms": max(samples),
                               "verified": result["verified"], "samples_ms": samples}
                        rows.append(row)
                        group.append(row)
                        print(f"  [{len(rows):3}/{total}] ✓ {name:12} {row['median_ms']:10.3f} ms  ({min(samples):.3f}–{max(samples):.3f})", flush=True)
                    maximum = max(r["median_ms"] for r in group) or 1
                    fastest = min(r["median_ms"] for r in group) or 1e-9
                    for row in group:
                        bar = "█" * max(1, round(row["median_ms"] / maximum * 32))
                        print(f"  {row['algorithm']:12} {bar:32} {row['median_ms']/fastest:6.1f}× fastest", flush=True)
                    save_report(args.output, rows, metadata, "Running")
    except Exception:
        status = "Failed (partial results)"
        raise
    finally:
        save_report(args.output, rows, metadata, status)
    print(f"\n✓ Report ready: {args.output / 'index.html'}", flush=True)


if __name__ == "__main__":
    main()
