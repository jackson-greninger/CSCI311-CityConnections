def digest(filename):
    """
    turns the file into a graph (dictionary)

    - keys are start node ID's
    - values are tuples: (end node ID, length/weight)
    """
    adjacency_list = {}
    edges = {}
    nodes = set()
    
    with open(filename, 'r') as file:

        for line in file:
            data = line.split()

            if len(data) != 4:
                continue
            
            eid, start, end, weight = data
            
            # coerce into proper type
            eid, start, end, weight = int(eid), int(start), int(end), float(weight)

            edges[eid] = (start, end, weight)
            nodes.update([start, end])

            # both directions - undirected graph
            adjacency_list.setdefault(start, []).append((end,   weight, eid))
            adjacency_list.setdefault(end,   []).append((start, weight, eid))
    
    return adjacency_list, edges, nodes

parsed_data = digest("SanJaoquin.txt")