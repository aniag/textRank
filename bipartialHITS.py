#!/usr/bin/python
# -*- coding: utf-8 -*-

import vertex
import math

class BipartialHITS(object):

    def __init__(self, authVertices, hubVertices, edges = {}):
        self._AuthVertices = authVertices
        self._HubVertices = hubVertices
        self._edges = edges
        if len(self._HubVertices) > 1:
            for v in self._HubVertices:
                v.setScore(1)
        else:
            print 'Empty graph!'

    def HITSiteration(self):
        for vrtx in self._AuthVertices:
            vrtx.ageScore()
        for vrtx in self._HubVertices:
            vrtx.ageScore()
        norm = 0
        for vrtx in self._AuthVertices:
            score = 0
            for neighbour in vrtx.getNeighbours():
                score += neighbour._score
            vrtx._score = score
            norm += pow(score, 2)
        norm = math.sqrt(norm)
        for vrtx in self._AuthVertices:
            score = vrtx._score * 1. / norm
            vrtx.setScore(score)
        for vrtx in self._HubVertices:
            score = 0
            for neighbour in vrtx.getNeighbours():
                score += neighbour._score
            vrtx._score = score
            norm += pow(score, 2)
        norm = math.sqrt(norm)
        for vrtx in self._HubVertices:
            score = vrtx._score * 1. / norm
            vrtx._score = score
        
            
                    
    def checkConvergence(self, threshold):
        for vertex in self._HubVertices:
            if vertex.getDiff() > threshold:
                return False
        return True
