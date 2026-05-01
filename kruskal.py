import sys
import time

class UnionFind:
    def __init__(self, nodes):
        self.parent = {}
        self.rank = {}

        for node in nodes:
            self.parent[node] = node
            
        for node in nodes:
            self.rank[node] = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # Detect cycles
        
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True

def read_graph(filename):
    edges = []
    nodes = set()

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            edge_id, start, end, length = line.split()
            edge_id = int(edge_id)
            start   = int(start)
            end     = int(end)
            length  = float(length)

            edges.append((length, edge_id, start, end))
            nodes.add(start)
            nodes.add(end)

    return edges, nodes


def write_mst(filename, mst_edges):
    with open(filename, 'w') as f:
        for (length, edge_id, start, end) in mst_edges:
            f.write(f"{edge_id} {start} {end} {length}\n")

def kruskal(edges, nodes):
    # Sort edges by weight ascending order
    edges.sort(key=lambda e: e[0])

    # Initialize Forest
    uf = UnionFind(nodes)
    mst_edges = []
    total_weight = 0.0

    # Iterate through sorted edges
    for (length, edge_id, start, end) in edges:
        # If start and end are in different components add this edge
        if uf.union(start, end): # If union is successful it means no cycle
            mst_edges.append((length, edge_id, start, end)) # Add edge to MST 
            total_weight += length
            # MST is complete when we have V-1 edges
            if len(mst_edges) == len(nodes) - 1:
                break

    return mst_edges, total_weight

def main():
    if len(sys.argv) != 3:
        print("Usage: python kruskal.py inputfile outputfile")
        sys.exit(1)

    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    edges, nodes = read_graph(input_file)

    # timing
    start_time = time.time()

    mst_edges, total_weight = kruskal(edges, nodes)

    end_time = time.time()
    elapsed = end_time - start_time

    write_mst(output_file, mst_edges)



    print(f"Nodes: {len(nodes)}")
    print(f"Edges in MST: {len(mst_edges)}")
    print(f"Total MST Weight: {total_weight}")
    print(f"Elapsed time: {elapsed}")


if __name__ == "__main__":
    main()