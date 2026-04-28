def digest(filename):
    """
    turns the file into a graph (dictionary)

    - keys are start node ID's
    - values are tuples: (end node ID, length/weight)
    """
    graph = {}
    
    with open(filename, 'r') as file:
        data = file.readlines()
    
        for line in data:
            edgeID, startID, endID, length = line.split()
            startID, endID, length = int(startID), int(endID), float(length)

            if startID not in graph:
                graph[startID] = []
            graph[startID].append((endID, length))
    return graph

parsed_data = digest("CSCI311-CityConnections\SanJaoquin.txt")

print(parsed_data[0])