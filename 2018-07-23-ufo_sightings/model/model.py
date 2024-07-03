import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def buildGraph(self, anno, xG):
        self._grafo.clear()
        allNodes = DAO.getAllStates()
        self._grafo.add_nodes_from(allNodes)
        for n in allNodes:
            self._idMap[n.id] = n
        self.addEdges(anno, xG)
        return True

    def addEdges(self, anno, xG):
        edges = DAO.getConnections(self._idMap)
        for e in edges:
            self._grafo.add_edge(e.s1, e.s2, weight=0)
        for s1, s2 in self._grafo.edges:
            peso = DAO.getPesi(s1.id, s2.id, anno, xG)
            self._grafo[s1][s2]["weight"] = peso

    def sumWeightNeighbours(self):
        viciniTuple = []
        for n in self._grafo.nodes:
            sumWeight = 0
            for n2 in self._grafo.nodes:
                if self._grafo.has_edge(n, n2):
                    for i in self._grafo[n][n2]['weight']:
                        sumWeight += int(i)
            viciniTuple.append((n.id, sumWeight))
        return viciniTuple

    def printGraphDetails(self):
        return f"Numero di nodi: {len(self._grafo.nodes)}; Numero di archi: {len(self._grafo.edges)}"
