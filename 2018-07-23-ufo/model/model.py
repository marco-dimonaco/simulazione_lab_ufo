import copy # 1
import networkx as nx
from geopy.distance import distance
from database.DAO import DAO


class Model:
    def __init__(self):
        self._bestdTot = None
        self._bestComp = None
        self._grafo = nx.Graph()
        self._idMap = {}

    def buildGraph(self, shape, year):
        allNodes = DAO.getAllStates()
        self._grafo.add_nodes_from(allNodes)
        for n in allNodes:
            self._idMap[n.id] = n
        self.addEdges(shape, year)
        return True

    def addEdges(self, shape, year):
        allEdges = DAO.getConnections(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.stato1, e.stato2, weight=0)
        for s1, s2 in self._grafo.edges:
            peso = DAO.getPesi(s1.id, s2.id, shape, year)
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

    def getPath(self):
        # caching con variabili della classe (percorso migliore e peso maggiore)
        self._bestComp = []
        self._bestdTot = 0
        # inizializzo il parziale con il nodo iniziale
        parziale = []

        for a in self._grafo.nodes:
            if a not in parziale:
                parziale.append(a)
                self._ricorsione(parziale)
                parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking
        return self._bestComp, self._bestdTot

    def _ricorsione(self, parziale):
        # verifico se soluzione è migliore di quella salvata in cache
        if self.getScore(parziale) > self._bestdTot:
            # se lo è aggiorno i valori migliori
            self._bestComp = copy.deepcopy(parziale)
            self._bestdTot = self.getScore(parziale)
        # verifico se posso aggiungere un altro elemento
        comp = self._grafo.neighbors(parziale[-1])
        for a in comp:
            if a not in parziale:
                if len(parziale) < 2:
                    parziale.append(a)
                    self._ricorsione(parziale)
                    parziale.pop()
                elif self._grafo[parziale[-1]][a]["weight"] > self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                    parziale.append(a)
                    self._ricorsione(parziale)
                    parziale.pop()  # rimuovo l'ultimo elemento aggiunto: backtracking

    def getScore(self, list):
        score = 0
        for i in range(0, len(list) - 1):
            score += distance((list[i].Lat, list[i].Lng), (list[i + 1].Lat, list[i + 1].Lng)).km
        return score

    def printGraphDetails(self):
        return f"Numero di vertici: {len(self._grafo.nodes)}; Numero di archi: {len(self._grafo.edges)}"

    @staticmethod
    def getShapes(anno):
        return DAO.getAllShapes(anno)
