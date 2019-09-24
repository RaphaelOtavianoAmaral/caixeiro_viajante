from grafo import Graph


CITIES = [('A', [('B', 3), ('C', 3), ('D', 3)]),
         ('B', [('C', 3), ('D', 4)]),
         ('C', [('D', 1)]),
         ('D', [])]
INT_MAX = 10000


# transforma o array CITIES em um grafo
def createMap():
    instanceMap = Graph()
    for vertex, neighbors in CITIES:
        if len(neighbors) > 0:
            for neighbor, cost in neighbors:
                instanceMap.addEdge(vertex, neighbor, cost)
    return instanceMap


# recebe um grafo completo e um nodo inicial
def nearestNeighborHeuristic(cities, start):
    path = [start]
    visited = [start]

    # percorre cada cidade do grafo
    for city in path:
        city = cities.getVertex(city)
        # remove os vizinhos já visitados
        neighborhood = dict(filter(lambda x: x[0] not in visited, city.connectedTo.items()))
        # se ainda existem nodos a serem visitados
        if neighborhood:
            # escolhe o que tem menor custo da lista
            nearest = min(neighborhood, key=lambda x: neighborhood.get(x))
            # marca como visitado
            visited.append(nearest)
            # inclui o menor como parte da solução
            path.append(nearest)
        # se não exite nodos a serem visitados
        else:
            # o caixeiro volta para a cidade inicial
            path.append(start)
            break
    return path


createdMap = createMap()
print(nearestNeighborHeuristic(createdMap, 'A'))