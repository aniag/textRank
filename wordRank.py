#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, math, string
import sentence
import morfeuszDB4GUI
import operator
import pageRank
import vertex



def update(window, vertices, edges):
    pass
    
def prepareGraph(source, morfo, POS, w_size, vertices, edges, sentences):
    src = open(source, 'r')
    num = 0
    for line in src:
        sent = sentence.Sentence(line, num)
        window = [[]]*w_size
        tokens = re.sub('['+string.punctuation+']', ' ', line).lower().split()
        for w in tokens:
            sent.addWord(w)
            vertBucket = []
            dummy = morfo.lookUpWord(w)
            if 'stopword' in [p for (b, p) in dummy]: continue
            for (base, pos) in dummy:            
                if pos in POS : 
                    vertBucket.append(vertex.WordVertex(base))
            window
            update(window, vertices, edges)
        sentences.append(sent)
        num += 1
    src.close()

def algorithm(source, morfo, POS, w_size, threshold):
    vertices = []
    edges = {}
    sentences = []
    prepareGraph(source, morfo, POS, w_size, vertices, edges, sentences)    
    pr = pageRank.PageRank(vertices, edges)
    while not pr.checkConvergence(threshold): pr.pageRankIteration()
    
    return vertices
