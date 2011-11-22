#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, string
import sentence
import morfeuszDB4GUI
import operator
import pageRank
import vertex
import graph

def prepareGraph(source, morfo, POS, sgraph):
    src = open(source, 'r')
    num = 0
    for line in src:
        sent = sentence.Sentence(line, num)
        tokens = re.sub('['+string.punctuation+']', ' ', line).lower().split()
        for w in tokens:
            dummy = morfo.lookUpWord(w)
            if 'stopword' in [p for (b, p) in dummy]: continue
            for (base, pos) in dummy:
                if pos in POS : sent.addWord(base)
        v = vertex.SentenceVertex(sent, num)
        sgraph.update(v)
        num += 1
    src.close()

def algorithm(source, morfo, POS, threshold):
    sgraph = graph.GraphOfSentences()
    prepareGraph(source, morfo, POS, sgraph)    
    pr = pageRank.PageRank(sgraph.getVertices(), sgraph.getEdges())
    while not pr.checkConvergence(threshold): pr.pageRankIteration()
    # vertices.sort(key=lambda v: v.getScore(), reverse=True)
    return dict([(v.getSentence().getOrdinalNumber(), v.getScore()) for v in sgraph.getVertices()])
    
#def main():
    

if __name__ == '__main__':
    #morfo = morfeuszDB4GUI.MorfeuszDB4GUI('/home/aglazek/mgr/morfeusz')
    morfo = morfeuszDB4GUI.MorfeuszDB4GUI('/home/aglazek/private/relacje_rozne/word_relations')
    print algorithm('/home/aglazek/private/teksty/czekan.txt', morfo, ['noun', 'verb', 'adjective', 'unknown'], 0.01)
