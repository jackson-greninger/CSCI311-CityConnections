from digest import digest
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
        # min is always at root
        top = heap[0] 
        size -= 1
        if size > 0:
            # move last entry to root, then sink it down
            heap[0] = heap.pop()
            i, n = 0, size               # fixed: = not -
            while True:
                left     = (i << 1) + 1
                right    = left + 1
                smallest = i
                if left  < n and heap[left][0]  < heap[smallest][0]: smallest = left   # fixed: smallest not s
                if right < n and heap[right][0] < heap[smallest][0]: smallest = right  # fixed: smallest not s
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
    for neighbor, weight, eid in adjacent_list.get(src, []):  # unpack 3 values
        push(weight, neighbor, eid)

    while size > 0:
        weight, node, eid = pop()
        # stale heap entry, skip
        if node in visited:
            continue
        visited.add(node)
        mst_edges.append(eid)            

        # push unvisited neighbors — cheapest will bubble to top
        for neighbor, w, neid in adjacent_list.get(node, []):  # unpack 3 values
            if neighbor not in visited:
                push(w, neighbor, neid)

    return mst_edges


#####################################
#for testing 

if __name__ == "__main__":
    adj_list, edges, nodes = digest("test.txt")
    mst = prims_algorithm(adj_list, nodes)

    total = 0
    for eid in mst:
        start, end, weight = edges[eid]
        print(f"edge {eid}: {start} -- {end}  weight {weight}")
        total += weight
    print(f"Total weight: {total}")