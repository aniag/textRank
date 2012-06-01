#!/usr/bin/python
# -*- coding: utf-8 -*-

# import vertex

class PageRank(object):

    def __init__(self, vertices, edges = {}, d = 0.05):
        self._vertices = vertices
        self._edges = edges
        self._d = d
        if len(vertices) > 1:
            for v in self._vertices:
                v.setOldScore(1)
                v.setScore(1)
                break
        else:
            print 'Empty graph!'

    def pageRankIteration(self):
        for vrtx in self._vertices:
            vrtx.ageScore()
        for vrtx in self._vertices:
            score = 0
            for neighbour in vrtx.getNeighbours():
                # score += neighbour.getOldScore() * self._edges[(vrtx, neighbour)] * 1./neighbour.getOutSum()
                score += neighbour._oldScore * self._edges[(vrtx, neighbour)] * 1./neighbour._outSum
            vrtx.setScore(self._d*1./len(self._vertices) + (1-self._d)*score)
            
    def checkConvergence(self, threshold):
        for vertex in self._vertices:
            if vertex.getDiff() > threshold:
                return False
        return True
