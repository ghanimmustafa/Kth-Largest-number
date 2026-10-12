# Kth-Largest-number
This project finds the Kth largest number of a data in a text file using several algorithms:

1- Insertion Sort Algorithm ( Sort All)

2- Sort only K-size Algorithm ( Sort K)

3- Sort Heap Algorithm ( Min Heap)

4- Quick Select Algorithm

The test speed performance changes widely between the first and the last algorithm from very slow to very fast. 
To create a test file, all the numbers have to be positive and integer. The first number in the text file will represent the algorithm type (1,2,3, or 4), the second number is the required K number, and the last number is the total number of elements N. 

## Visual performance benchmarks

[![Algorithm performance](https://github.com/ghanimmustafa/Kth-Largest-number/actions/workflows/performance.yml/badge.svg)](https://github.com/ghanimmustafa/Kth-Largest-number/actions/workflows/performance.yml)

Every push and pull request runs all four implementations on the same seeded inputs. In **Actions → Algorithm performance**, open **Live algorithm comparison → Benchmark · live timings and charts** to watch verified timings, progress counters and comparison bars arrive as each scenario completes.

When the job finishes, its summary shows median timings, sample ranges and relative speeds. Download the **algorithm-performance** artifact and open `index.html` for a dark themed report with input size and distribution filters. The report works offline and includes SVG charts, CSV results and JSON with every timing sample. Reports are retained for 30 days.

Use **Run workflow** to customize input sizes and repetitions. Defaults are N = 1,000 / 5,000 / 20,000, K ≈ 1% / 50%, five measured repetitions and one warmup. Random, ascending, descending and duplicate-heavy inputs expose different algorithm behavior. Boundary cases are verified before timing, and every measured result is checked against a fully sorted reference.

Live updates appear in the log; GitHub renders the summary after the job finishes. Timings measure the existing `select()` methods, including input parsing, allocation and captured output, while excluding process startup, data generation and reference sorting. Shared runner load can affect results, so compare large differences and sample ranges rather than treating tiny changes as regressions.

Run the same report locally with Python 3 and a C++17 compiler; no Python packages are required:

```bash
mkdir -p build
g++ -std=c++17 -O2 -I. benchmarks/runner.cpp \
  SelectionAlgorithm.cpp AlgorithmSortAll.cpp AlgorithmSortK.cpp \
  AlgorithmSortHeap.cpp AlgorithmSortQuick.cpp BinaryHeap.cpp -o build/benchmark
python3 benchmarks/report.py --binary build/benchmark --check
python3 -u benchmarks/report.py --binary build/benchmark
```

For a shorter custom run:

```bash
BENCHMARK_SIZES=100,1000 BENCHMARK_REPEATS=3 \
  python3 -u benchmarks/report.py --binary build/benchmark
```
