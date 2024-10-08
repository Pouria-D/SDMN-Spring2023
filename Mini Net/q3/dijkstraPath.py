def initial_graph():

    return {
        '1': {'2': 2, '3': 3, '4': 4},
        '2': {'1': 2, '4': 1},
        '3': {'1': 3},
        '4': {'1': 1, '2': 1}
    }


def calculatePath(initialGraph, source, dest):
    path = {}
    adj_node = {}
    queue = []
    graph = initialGraph

    for node in graph:
        path[node] = float("inf")
        adj_node[node] = None
        queue.append(node)

    path[source] = 0

    while queue:
        # find min distance which wasn't marked as current
        key_min = queue[0]
        min_val = path[key_min]
        for n in range(1, len(queue)):
            if path[queue[n]] < min_val:
                key_min = queue[n]
                min_val = path[key_min]
        cur = key_min
        queue.remove(cur)

        for i in graph[cur]:
            alternate = graph[cur][i] + path[cur]
            if path[i] > alternate:
                path[i] = alternate
                adj_node[i] = cur

    path = [dest]
    x = dest
   # print(f'The path between {source} to {dest}')
   # print(x, end='<-')
    while True:
        x = adj_node[x]
        if x is None:
     #       print("")
            break
     #   print(x, end='<-')
        path.append(x)

    path.reverse()
    return path


# print(initial_graph())
# print(calculatePath(initialGraph=initial_graph(), source='1', dest='4'))

