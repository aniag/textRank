#!/usr/bin/python
# -*- coding: utf-8 -*-

# import vertex

class PageRank(object):

    def __init__(self, vertices = [], edges = {}, d = 0.1):
        self._vertices = vertices
        self._edges = edges
        self._d = d

    def pageRankIteration(self):
        for vrtx in self.vertices:
            score = 0
            for neighbour in vrtx.getNeighbours():
                score += neighbour.getOldScore() * self.edges[(vrtx, neighbour)] * 1./neighbour.getOutSum()
            vrtx.setScore(self._d + (1-self._d)*score)
            
    def addEdge(self, v, w, weight):
        if (v, w) not in self._edges:
            self._edges[(v, w)] = weight
            self._edges[(w, v)] = weight
        else: assert(self._edges[(v, w)] == weight)
        
    def checkConvergence(self, threshold):
        for vertex is self._vertices:
            if vertex.getDiff() > threshold:
                return False
        return True
