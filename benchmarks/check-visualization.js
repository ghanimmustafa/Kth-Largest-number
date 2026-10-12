// Validate the stepwise algorithms without animation or a browser dependency.
const assert = require('node:assert/strict');
const { algorithms, dataset } = require('./algorithms.js');
let cases = 0;
for (const n of [1, 2, 9, 10, 11, 12, 32, 64, 128, 256]) {
  for (const distribution of ['random', 'ascending', 'descending', 'duplicates']) {
    for (const seed of [0, 2026, 4811]) {
      const input = dataset(n, distribution, seed);
      for (const k of new Set([1, Math.max(1, Math.floor(n / 2)), n])) {
        const expected = [...input].sort((a, b) => b - a)[k - 1];
        for (const algorithm of algorithms) {
          const iterator = algorithm([...input], k);
          let next, steps = 0;
          do {
            next = iterator.next();
            assert.ok(++steps < 200000, 'Algorithm should terminate');
          } while (!next.done);
          assert.equal(next.value, expected, `${algorithm.name}, N=${n}, K=${k}, ${distribution}, seed=${seed}`);
          assert.deepEqual(input, dataset(n, distribution, seed), 'Each algorithm uses a copy');
          cases++;
        }
      }
    }
  }
}
console.log(`PASS: ${cases} browser algorithm cases, verified against sorted inputs`);

// Exercise benchmark-sized inputs and K=N without billions of quadratic shifts.
for (const n of [1000, 5000, 20000, 50000]) {
  const input = dataset(n, 'descending', 2026);
  for (const k of new Set([1, Math.floor(n / 2), n])) {
    for (const algorithm of algorithms) {
      const iterator = algorithm([...input], k);
      let next, steps = 0;
      do {
        next = iterator.next();
        assert.ok(++steps < 10000000, 'Large input should terminate');
      } while (!next.done);
      assert.equal(next.value, input[k - 1], `${algorithm.name}, N=${n}, K=${k}`);
    }
  }
}
console.log('PASS: all four algorithms at N=1,000 / 5,000 / 20,000 / 50,000 with K=1 / N/2 / N');
