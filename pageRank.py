#!/usr/bin/python
# -*- coding: utf-8 -*-

def pageRankIteration(vertices, edges, d):
    for vrtx in vertices:
        score = 0
        for neighbour in vrtx.getNeighbours():
            score += neighbour.getOldScore() * edges[(vrtx, neighbour)] * 1./neighbour.getOutSum()
        vrtx.setScore(d + (1-d)*score)
