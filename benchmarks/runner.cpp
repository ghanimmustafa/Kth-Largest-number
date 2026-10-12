#include "AlgorithmSortAll.h"
#include "AlgorithmSortK.h"
#include "AlgorithmSortHeap.h"
#include "AlgorithmSortQuick.h"
#include <algorithm>
#include <chrono>
#include <memory>
#include <random>
#include <sstream>
#include <vector>

// Exercise the actual select() implementations, including their input parsing.
int main(int argc, char** argv) {
    if (argc != 7) return 2;
    int type = std::stoi(argv[1]), n = std::stoi(argv[2]);
    int k = std::stoi(argv[3]), repeats = std::stoi(argv[6]);
    std::string distribution = argv[5];
    if (type < 1 || type > 4 || n < 1 || k < 1 || k > n || repeats < 1) return 2;
    std::mt19937 rng(std::stoul(argv[4]));
    std::uniform_int_distribution<int> random(1, 1000000);
    std::vector<int> values(n);
    for (int& value : values) value = distribution == "duplicates" ? random(rng) % 8 + 1 : random(rng);
    if (distribution == "ascending") std::sort(values.begin(), values.end());
    else if (distribution == "descending") std::sort(values.rbegin(), values.rend());
    else if (distribution != "random" && distribution != "duplicates") return 2;
    auto sorted = values;
    std::sort(sorted.rbegin(), sorted.rend());
    int expected = sorted[k - 1];
    std::ostringstream input;
    input << n << '\n';
    for (int value : values) input << value << ' ';
    std::vector<double> samples;
    // One untimed warmup, then independent runs of the same input.
    for (int trial = -1; trial < repeats; ++trial) {
        std::unique_ptr<SelectionAlgorithm> algorithm;
        if (type == 1) algorithm.reset(new AlgorithmSortAll(k));
        if (type == 2) algorithm.reset(new AlgorithmSortK(k));
        if (type == 3) algorithm.reset(new AlgorithmSortHeap(k));
        if (type == 4) algorithm.reset(new AlgorithmSortQuick(k));
        std::istringstream stream(input.str());
        std::ostringstream output;
        std::cin.clear();
        auto* original_in = std::cin.rdbuf(stream.rdbuf());
        auto* original_out = std::cout.rdbuf(output.rdbuf());
        auto start = std::chrono::steady_clock::now();
        int result = algorithm->select();
        auto end = std::chrono::steady_clock::now();
        std::cin.rdbuf(original_in);
        std::cout.rdbuf(original_out);
        std::cin.clear();
        if (result != expected) {
            std::cerr << "Incorrect result: expected " << expected << ", got " << result << '\n';
            return 1;
        }
        if (trial >= 0) samples.push_back(std::chrono::duration<double, std::milli>(end - start).count());
    }
    std::cout << "{\"verified\":true,\"samples_ms\":[";
    for (size_t i = 0; i < samples.size(); ++i) std::cout << (i ? "," : "") << samples[i];
    std::cout << "]}\n";
}
