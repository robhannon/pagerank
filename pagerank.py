import random as r
import numpy as n
import copy as c
import pandas as p

class Graph:
    def __init__(self):
        self.graph = {}
        self.inverted = {}

    def add_node(self, name):
        if name not in self.graph:
            self.graph[name] = []
            self.inverted[name] = []
            
    def add_edge(self, node1, node2):
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1].append(node2)
            self.inverted[node2].append(node1)

    def neighbors(self, node):
        return self.graph[node]
    
    def print_nodes(self):
        for x in self.graph.keys():
            print(x)
    
    def print_edges(self):
        for x in self.graph.keys():
            for y in self.graph[x]:
                print((x, y))
            
    def length(self):
        return len(self.graph.keys())
        
    def rw(self):
        rw_graph = {}
        for x in self.graph.keys():
            rw_graph[x] = 0
        start = r.choice(list(rw_graph.keys()))
        rw_graph[start] = 1
        for x in range(10000):
            choices = self.neighbors(start)
            if len(choices) == 0 or (r.random() > .85):
                start = r.choice(list(rw_graph.keys()))
            else:
                start = r.choice(choices)
            rw_graph[start] += 1
        for x in rw_graph.keys():
            rw_graph[x] /= 10000
        rank = sorted(rw_graph.items(), key=lambda item:item[1], reverse=True)
        return rank
    
    def convergence_test(self, past, current):
        test = True
        for a in past.keys():
            if round(past[a], 3) != round(current[a], 3):
                test = False
                break
        return test

    def pr_iterate(self):
        current = {}
        past = {}
        d = .85
        length = self.length()
        for x in self.graph.keys():
            current[x] = float(1/length)
        past = c.deepcopy(current)
        for iterations in range(100):
            print(iterations)
            for y in past.keys():
                summation = 0
                for z in self.inverted[y]:
                    summation += past[z]/len(self.neighbors(z))
                current[y] = summation
                #current[y] = ((1 - d)/length) + (d * summation)
            if self.convergence_test(past, current) == True:
                break
            else:
                past = c.deepcopy(current)
        rank = sorted(current.items(), key=lambda item:item[1], reverse=True)
        return rank
    
    def matrix_convergence_test(self, past, current):
        test = True
        for x in range(len(past)):
            if round(past[x], 3) != round(current[x], 3):
                test = False
                break
        return test

    def pr_matrix(self):
        matrix = []
        for x in self.graph.keys():
            arr = []
            for y in self.graph.keys():
                if x not in self.graph[y]:
                    arr.append(0)
                else:
                    arr.append(.85*(1/len(self.neighbors(y))))
            matrix.append(arr)
        matrix = matrix + (.15/self.length() * n.ones((self.length(), self.length())))
        x = []
        for y in range(self.length()):
            x.append(1/self.length())
        for iterations in range(100):
            print(iterations)
            if self.matrix_convergence_test(x, (matrix @ x)):
                break
            x = matrix @ x
        rank = {}
        node = 0
        for a in self.graph.keys():
            rank[a] = x[node]
            node += 1
        rank = sorted(rank.items(), key=lambda item:item[1], reverse=True)
        return rank
        
    
g = Graph()
g.add_node('a')
g.add_node('b')
g.add_node('c')
g.add_node('d')
g.add_edge('a','b')
g.add_edge('b','a')
g.add_edge('b','c')
g.add_edge('b','d')
g.add_edge('c','a')
g.add_edge('d','c')
print(g.graph)

#g.print_edges()
#print(g.rw())
print(g.pr_iterate())
print(g.pr_matrix())

df = p.read_csv('/Users/roberthannon/nfl.txt')

nfl = Graph()
for i in range(len(df)):
    nfl.add_node(df.loc[i, "Winner/tie"])
    nfl.add_node(df.loc[i, "Loser/tie"])
    if int(df.loc[i, "Pts"]) > int(df.loc[i, "Pts.1"]):
        nfl.add_edge((df.loc[i, "Loser/tie"]), (df.loc[i, "Winner/tie"]))
print(nfl.pr_iterate())



        