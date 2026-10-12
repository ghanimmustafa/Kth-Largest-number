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
from urllib.parse import urlencode

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


def summary_charts(rows):
    """Public image URLs let GitHub render charts without hosting repo files.

    Only algorithm names, dataset sizes and median durations go to QuickChart.
    Raw samples, runner metadata and commit identifiers stay in the artifact.
    """
    complete = {}
    for row in rows:
        key = (row["n"], row["k"], row["distribution"])
        complete.setdefault(key, {})[row["id"]] = row
    complete = {key: group for key, group in complete.items() if len(group) == 4}
    if not complete:
        return []
    largest = max(key[0] for key in complete)
    markdown = ["### Performance charts", "", f"Largest input: **N = {largest:,}** · median milliseconds · shorter bars are faster.", ""]
    for distribution in DISTRIBUTIONS:
        ks = sorted(k for n, k, d in complete if n == largest and d == distribution)
        if not ks:
            continue
        config = {
            "type": "bar",
            "data": {
                "labels": [f"K = {k:,} ({100*k/largest:g}%)" for k in ks],
                "datasets": [{"label": name, "data": [round(complete[(largest, k, distribution)][i]["median_ms"], 6) for k in ks],
                              "backgroundColor": COLORS[i], "borderRadius": 4} for i, name in NAMES.items()],
            },
            "options": {
                "indexAxis": "y",
                "plugins": {
                    "title": {"display": True, "text": f"{distribution.title()} inputs · N = {largest:,}", "color": "#e2e8f0", "font": {"size": 20}},
                    "legend": {"labels": {"color": "#cbd5e1"}},
                },
                "scales": {
                    "x": {"beginAtZero": True, "title": {"display": True, "text": "Median duration (ms)", "color": "#94a3b8"},
                          "ticks": {"color": "#94a3b8"}, "grid": {"color": "#26324a"}},
                    "y": {"ticks": {"color": "#cbd5e1"}, "grid": {"display": False}},
                },
            },
        }
        url = "https://quickchart.io/chart?" + urlencode({
            "version": "4", "format": "png", "width": 900, "height": 360,
            "backgroundColor": "#111b2e", "c": json.dumps(config, separators=(",", ":")),
        })
        markdown.extend([f"![{distribution.title()} algorithm comparison, N={largest:,}; median milliseconds]({url})", ""])
    markdown.extend(["Charts use QuickChart image rendering. Exact values for every size are in the table below; offline charts are included in the artifact.", ""])
    return markdown


def save_report(output, rows, metadata, status):
    output.mkdir(parents=True, exist_ok=True)
    (output / "results.json").write_text(json.dumps({"metadata": metadata, "status": status, "results": rows}, indent=2))
    fields = ("algorithm", "n", "k", "distribution", "median_ms", "min_ms", "max_ms", "verified")
    with (output / "results.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    summary = ["## ⚡ Algorithm performance", f"**{status}** · {len(rows)} measurements · {metadata['repeats']} repetitions + one warmup", "",
               "Times include input parsing, allocation, selection and captured output; exclude process startup and dataset generation. All results are checked against a sorted reference. Shared runner timings can vary between runs.", ""]
    summary.extend(summary_charts(rows))
    summary.extend(["<details>", "<summary>View all timings, sample ranges and relative speeds</summary>", "",
               "| Input | K | Distribution | Algorithm | Median (ms) | Range (ms) | vs fastest |", "|---:|---:|---|---|---:|---:|---:|"]
    )
    groups = {}
    for row in rows:
        key = (row["n"], row["k"], row["distribution"])
        groups.setdefault(key, []).append(row)
    for index, ((n, k, distribution), group) in enumerate(groups.items()):
        fastest = min(r["median_ms"] for r in group) or 1e-9
        for row in group:
            summary.append(f"| {n:,} | {k:,} | {distribution} | {row['algorithm']} | {row['median_ms']:.3f} | {row['min_ms']:.3f}–{row['max_ms']:.3f} | {row['median_ms']/fastest:.1f}× |")
        title = f"{distribution.title()} · N = {n:,} · K = {k:,}"
        svg = chart(group, title)
        (output / f"chart-{index+1:02d}.svg").write_text(svg)
    summary.extend(["", "</details>", "", "Download the **algorithm-performance** artifact for the interactive report, SVG charts, CSV and individual timing samples."])
    markdown = "\n".join(summary) + "\n"
    (output / "summary.md").write_text(markdown)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        Path(os.environ["GITHUB_STEP_SUMMARY"]).write_text(markdown)
    payload = json.dumps({"metadata": metadata, "status": status, "results": rows}, separators=(",", ":")).replace("<", "\\u003c")
    template = Path(__file__).with_name("view.html").read_text()
    algorithms = Path(__file__).with_name("algorithms.js").read_text()
    page = template.replace("__ALGORITHM_CODE__", algorithms).replace("__BENCHMARK_DATA__", payload)
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
                "commit": os.getenv("GITHUB_SHA", "local"),
                "run_url": f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{os.getenv('GITHUB_REPOSITORY', 'ghanimmustafa/Kth-Largest-number')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}" if os.getenv("GITHUB_RUN_ID") else "",
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
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
