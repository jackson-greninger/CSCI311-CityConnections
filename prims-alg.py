import sys
from digest import digest
import time

def prims_algorithm(adjacent_list, nodes):
    visited   = set()
    mst_edges = []
    heap      = []
    size      = 0

    def push(weight, node, eid):
        nonlocal size
        heap.append((weight, node, eid))
        i = size
        size += 1
        # bubble new entry up until parent is smaller
        while i > 0:
            parent = (i - 1) // 2
            if heap[i] < heap[parent]:
                heap[i], heap[parent] = heap[parent], heap[i]
                i = parent
            else:
                break

    def pop():
        nonlocal size
        top = heap[0]       # min is always at root
        size -= 1
        if size > 0:
            heap[0] = heap.pop()    # move last entry to root, then sink it down
            i, n = 0, size
            while True:
                left     = (i << 1) + 1
                right    = left + 1
                smallest = i
                if left  < n and heap[left][0]  < heap[smallest][0]: smallest = left
                if right < n and heap[right][0] < heap[smallest][0]: smallest = right
                if smallest == i:
                    break
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
        else:
            heap.pop()
        return top

    # seed heap with all edges leaving the starting node
    src = next(iter(nodes))
    visited.add(src)
    for neighbor, weight, eid in adjacent_list.get(src, []):
        push(weight, neighbor, eid)

    while size > 0:
        weight, node, eid = pop()

        if node in visited:     # stale heap entry, skip
            continue

        visited.add(node)
        mst_edges.append(eid)

        # push unvisited neighbors — cheapest will bubble to top
        for neighbor, w, neid in adjacent_list.get(node, []):
            if neighbor not in visited:
                push(w, neighbor, neid)

    return mst_edges


if __name__ == "__main__":
    # testing
    if len(sys.argv) == 1:
        adj_list, edges, nodes = digest("test.txt")

        start = time.time()
        mst = prims_algorithm(adj_list, nodes)
        end = time.time()
        elapsed = end - start

        total = 0
        for eid in mst:
            start, end, weight = edges[eid]
            #print(f"edge {eid}: {start} -- {end}  weight {weight}")
            total += weight
        print(f"Total weight: {total}")

    elif len(sys.argv) == 3:
        adj_list, edges, nodes = digest(sys.argv[1])

        start = time.time()
        mst = prims_algorithm(adj_list, nodes)
        end = time.time()
        elapsed = end - start
        
        total_weight = 0
        total_nodes = 0
        total_edges = 0

        with open(sys.argv[2], 'r') as f:
            for eid in mst:
                start, end, weight = edges[eid]
                total_weight += weight
                total_edges += 1

        print(f"Nodes: {len(nodes)}")
        print(f"Edges in MST: {total_edges}")
        print(f"Total MST Weight: {total_weight}")
        print(f"Elapsed time: {elapsed}")

    else:
        print("Usage: python prims-alg.py inputfile outputfile")