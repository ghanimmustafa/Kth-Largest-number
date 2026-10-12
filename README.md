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

When the job finishes, open the run's **Summary** page to see colored bar charts for all four distributions at the largest input size, comparing both K values. Expand **View all timings, sample ranges and relative speeds** for the complete results. Summary chart images use QuickChart and send only algorithm labels, input sizes and median durations to that service; raw samples and runner metadata remain in the artifact.

Download the **algorithm-performance** artifact and open `index.html` for the interactive algorithm lab. Click **Run algorithms** to execute all four JavaScript visualizations side by side on identical inputs. Enter 1–50,000 elements and any K from 1 to N; pause, resume, step or change animation speed. **Use this input above** copies a C++ benchmark scenario into the browser controls. Large inputs use grouped display bars while processing every element; Turbo advances work in bounded batches so pause/reset remain available. The quadratic algorithms can take much longer on large inputs. Each result is checked against sorted input. Browser compute times and visual step counts describe the demonstration, while the separate **Measured in GitHub Actions** panel shows actual C++ measurements. The HTML works offline, with SVG charts, CSV results and JSON samples alongside it. Reports are retained for 30 days.

### Open the rendered HTML online

GitHub Actions summaries support Markdown and images, but cannot execute an interactive HTML/JavaScript app. The workflow can publish the lab to GitHub Pages and add an **Open the interactive algorithm view** link to the Actions summary.

1. Push the workflow and files in `benchmarks/` to GitHub.
2. Open **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**.
3. Open **Actions → Algorithm performance → Run workflow** on the default branch. Check **Publish the interactive HTML view**, then run it.
4. After publication, click **Open the interactive algorithm view** in the run summary and press **Run algorithms**.

To refresh the hosted C++ results automatically after each successful default-branch run, add a repository Actions variable named `PUBLISH_PERFORMANCE_VIEW` with value `true` in **Settings → Secrets and variables → Actions → Variables**. Pull requests do not deploy the site.

The browser actually executes the visualized algorithms, with animation slowed for readability. It does not stream the remote C++ process; hosted C++ results update when a benchmark workflow finishes and publishes.

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
