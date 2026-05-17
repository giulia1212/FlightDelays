# questo file testa il mio Model

from model.model import Model

myModel = Model()
myModel.buildGraph(5)
nNodes, nEdges = myModel.getGraphDetails()  # getGraphDetails() è un metodo del Model che mi restituisce il numero nodi e numero archi del grafo
# print(f"Num nodes: {nNodes}, num edges: {nEdges}")
