#!/usr/bin/python
# -*- coding: utf-8 -*-

# import vertex

class PageRank(object):

    def __init__(self, vertices = [], edges = {}, d = 0.05):
        self._vertices = vertices
        self._edges = edges
        self._d = d
        if len(vertices) > 1:
            self._vertices[0].setOldScore(1)
            self._vertices[0].setScore(1)
        else:
            print 'Empty graph!'

    def pageRankIteration(self):
        for vrtx in self._vertices:
            vrtx.ageScore()
        for vrtx in self._vertices:
            score = 0
            for neighbour in vrtx.getNeighbours():
                if(self._edges[(vrtx, neighbour)] != 0):
                    score += neighbour.getOldScore() * self._edges[(vrtx, neighbour)] * 1./neighbour.getOutSum()
            vrtx.setScore(self._d*1./len(self._vertices) + (1-self._d)*score)
            
    def addEdge(self, v, w, weight):
        if (v, w) not in self._edges:
            self._edges[(v, w)] = weight
            self._edges[(w, v)] = weight
        else: assert(self._edges[(v, w)] == weight)
        
    def checkConvergence(self, threshold):
        for vertex in self._vertices:
            if vertex.getDiff() > threshold:
                return False
        return True
