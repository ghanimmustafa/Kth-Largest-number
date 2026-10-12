/* Stepwise browser implementations for visualization, independent of CI timing. */
(function (root) {
  'use strict';
  function* sortAll(a, k) {
    for (let i = 1; i < a.length; i++) {
      const key = a[i]; let j = i - 1;
      while (j >= 0) {
        yield { active: [j, j + 1], phase: 'Comparing insertion position' };
        if (a[j] >= key) break;
        a[j + 1] = a[j]; j--;
        yield { active: [j + 1], phase: 'Shifting the sorted prefix' };
      }
      a[j + 1] = key;
      yield { active: [j + 1], phase: 'Inserting into descending order' };
    }
    return a[k - 1];
  }
  function* sortK(a, k) {
    const top = a.slice(0, k);
    for (const event of sortAll(top, k)) yield { ...event, view: top };
    yield { view: top, phase: 'Top K initialized' };
    for (let i = k; i < a.length; i++) {
      yield { view: top, active: [k - 1], phase: `Reading input ${i + 1} / ${a.length}` };
      if (a[i] <= top[k - 1]) continue;
      top[k - 1] = a[i];
      let j = k - 1;
      while (j > 0) {
        yield { view: top, active: [j, j - 1], phase: 'Finding position in top K' };
        if (top[j] <= top[j - 1]) break;
        [top[j], top[j - 1]] = [top[j - 1], top[j]]; j--;
      }
      yield { view: top, active: [j], phase: 'Top K updated' };
    }
    return top[k - 1];
  }
  function* minHeap(a, k) {
    const heap = [];
    function* insert(value) {
      heap.push(value); let hole = heap.length - 1;
      yield { view: heap, active: [hole], phase: 'Inserting into min heap' };
      while (hole > 0) {
        const parent = Math.floor((hole - 1) / 2);
        yield { view: heap, active: [parent, hole], phase: 'Comparing parent and child' };
        if (heap[parent] <= heap[hole]) break;
        [heap[parent], heap[hole]] = [heap[hole], heap[parent]]; hole = parent;
      }
    }
    for (let i = 0; i < k; i++) yield* insert(a[i]);
    for (let i = k; i < a.length; i++) {
      yield { view: heap, active: [0], phase: `Reading input ${i + 1} / ${a.length}` };
      if (a[i] <= heap[0]) continue;
      // Match the original implementation's deleteMin followed by insert.
      heap[0] = heap[heap.length - 1]; heap.pop();
      let hole = 0;
      while (2 * hole + 1 < heap.length) {
        let child = 2 * hole + 1;
        if (child + 1 < heap.length && heap[child + 1] < heap[child]) child++;
        yield { view: heap, active: [hole, child], phase: 'Restoring heap order' };
        if (heap[hole] <= heap[child]) break;
        [heap[hole], heap[child]] = [heap[child], heap[hole]]; hole = child;
      }
      yield* insert(a[i]);
    }
    return heap[0];
  }
  function* quickSelect(a, k) {
    const target = k - 1;
    function* select(left, right) {
      if (right - left + 1 <= 10) {
        for (let i = left + 1; i <= right; i++) {
          const key = a[i]; let j = i - 1;
          while (j >= left) {
            yield { active: [j, j + 1], phase: 'Sorting a small partition' };
            if (a[j] >= key) break;
            a[j + 1] = a[j]; j--;
          }
          a[j + 1] = key;
          yield { active: [j + 1], phase: 'Small partition updated' };
        }
        return a[target];
      }
      const center = Math.floor((left + right) / 2);
      for (const [x, y] of [[left, center], [left, right], [center, right]]) {
        yield { active: [x, y], phase: 'Choosing the median-of-three pivot' };
        if (a[y] > a[x]) [a[x], a[y]] = [a[y], a[x]];
      }
      [a[center], a[right - 1]] = [a[right - 1], a[center]];
      const pivot = a[right - 1]; let i = left, j = right - 1;
      while (true) {
        do { i++; yield { active: [i, right - 1], phase: 'Scanning above pivot' }; } while (a[i] > pivot);
        do { j--; yield { active: [j, right - 1], phase: 'Scanning below pivot' }; } while (a[j] < pivot);
        if (i >= j) break;
        [a[i], a[j]] = [a[j], a[i]];
        yield { active: [i, j], phase: 'Swapping across the partition' };
      }
      [a[i], a[right - 1]] = [a[right - 1], a[i]];
      yield { active: [i], phase: 'Pivot in its final position' };
      if (target === i) return pivot;
      return yield* select(target < i ? left : i + 1, target < i ? i - 1 : right);
    }
    return yield* select(0, a.length - 1);
  }
  function dataset(n, distribution, seed) {
    let state = seed >>> 0;
    const a = Array.from({ length: n }, () => {
      state = (Math.imul(1664525, state) + 1013904223) >>> 0;
      return 1 + state % (distribution === 'duplicates' ? 8 : 1000);
    });
    if (distribution === 'ascending') a.sort((x, y) => x - y);
    if (distribution === 'descending') a.sort((x, y) => y - x);
    return a;
  }
  const api = { algorithms: [sortAll, sortK, minHeap, quickSelect], dataset };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SelectionLab = api;
})(globalThis);
