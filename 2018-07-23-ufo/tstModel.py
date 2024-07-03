from model.model import Model

mymodel = Model()
mymodel.buildGraph('circle', 2010)
print(mymodel.printGraphDetails())
for n1 in mymodel._grafo.nodes:
    for n2 in mymodel._grafo.nodes:
        if mymodel._grafo.has_edge(n1, n2):
            print(mymodel._grafo[n1][n2]['weight'])

            # 1
