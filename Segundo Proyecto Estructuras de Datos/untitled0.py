# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:26:13 2020

@author: Joaquin
"""

from dijkstra import Graph, DijkstraSPF

A,B,C,D,E,F,G = nodos = list("ABCDEFG")

grafo = Graph()

grafo.add_edge(F, C, 15)
grafo.add_edge(F, B, 5)
grafo.add_edge(F, E, 40)

grafo.add_edge(E, G, 10)
grafo.add_edge(E, B, 20)

grafo.add_edge(D, B, 40)
grafo.add_edge(D, G, 45)
grafo.add_edge(D, F, 10)
grafo.add_edge(D, E, 35)

grafo.add_edge(C, E, 5)
grafo.add_edge(C, G, 25)

grafo.add_edge(A, G, 75)
grafo.add_edge(A, D, 20)


graph_dijkstra = DijkstraSPF(grafo, A)

for i in nodos:
    print("%-5s %7d" % (i, graph_dijkstra.get_distance(i)))
print("Caminos:")
print(" -> ".join(graph_dijkstra.get_path(B)))
print(" -> ".join(graph_dijkstra.get_path(C)))
print(" -> ".join(graph_dijkstra.get_path(D)))
print(" -> ".join(graph_dijkstra.get_path(E)))
print(" -> ".join(graph_dijkstra.get_path(F)))
print(" -> ".join(graph_dijkstra.get_path(G)))