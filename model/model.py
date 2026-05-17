import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()   # creo il grafo, semplice, non orientato e pesato, quindi va bene Graph()
        self._airports = DAO.getAllAirports()  # così ho tutti gli aeroporti presenti nel database, anche quelli in cui volano meno di 5 compagnie
        # creo idMap, la passo poi come argomento nel metodo getAllNodes del DAO
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a   # ad ogni id corrisponde un aeroporto

    def buildGraph(self, nMin):    # prende come parametro il numero minimo di aeroporti che viene fornito dall'utente
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)  # qui ci aspettiamo di avere i nodi già filtrati, quindi li posso aggiungere al grafo
        self._graph.add_nodes_from(nodes)
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        # self.addEdges()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        # self._graph.clear_edges()
        self.addEdgesV2()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")


    def addEdges(self):   # va a leggere tutte le tratte del database
        # Queste tratte hanno due problemi:
        #   1) ho archi diretti e inversi, quindi dovrò fare la somma a mano
        #   2) ho archi tra aeroporti che avevo filtrato
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:  # se fanno parte del sottoinsieme di nodi che mi serve
                # allora posso aggiungerlo
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):  # se arco esiste già incremento solo peso
                    self._graph[t.aeroportoP][t.aeroportoA]["weight"] += t.peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight = t.peso)

    def addEdgesV2(self):
        allTratte = DAO.getAllEdgesV2(self._idMapAirports)
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight = t.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        nodes =  list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes