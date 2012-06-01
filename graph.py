#!/usr/bin/python
# -*- coding: utf-8 -*-


class Graph(object):
    def __init__(self):
        self._vertices = set()
        self._edges = {}
        
    def addVertex(self, v):
        self._vertices.add(v)
        
    def getVertices(self):
        return self._vertices
        
    def addEdge(self, v1, v2, weight):
        v1.incOutSum(weight)
        v2.incOutSum(weight)
        weight += self._edges.get((v1, v2), 0)
        self._edges[(v1,v2)] = weight
        self._edges[(v2,v1)] = weight
        v1.addNeighbour(v2)
        v2.addNeighbour(v1)

    
    def getEdges(self):
        return self._edges

class GraphOfSentences(Graph):
    
    def _init_(self):
        Graph.__init__(self)
             
    def update(self, v):
        for u in self._vertices:
            w = u.similarity(v)
            if w > 0:
                self.addEdge(u, v, w)
        self.addVertex(v)
        
class GraphOfWords(Graph):

    def __init__(self, w_size):
        Graph.__init__(self)
        self._windowSize = w_size
        self._window = [[]] * self._windowSize
        
    def moveWindow(self):
        for i in range(self._windowSize - 1):
            self._window[i] = self._window[i+1]
        
    def addToWindow(self, vSet):
        self.moveWindow()
        self._window[-1] = vSet
    
    def update(self):
        for vrx in self._window[-1]:
            self.addVertex(vrx)
            for i in range(self._windowSize):
                for pred in self._window[i]:
                    w = (i+1)*1.0/self._windowSize
                    self.addEdge(vrx, pred, w)

class BipartialMixedGraph(Graph):
    def __init__(self):
        self._SentenceVertices = set()
        self._WordVertices = set()
        self._edges = {}
        
    def addSentenceVertex(self, v):
        self._SentenceVertices.add(v)
        
    def addWordVertex(self, v):
        self._WordVertices.add(v)
        
    def getSentenceVertices(self):
        return self._SentenceVertices
        
    def getWordVertices(self):
        return self._WordVertices
