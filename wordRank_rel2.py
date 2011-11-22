#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, string
import sentence
import morfeuszDB4GUI
import operator
import pageRank
import vertex
import graph



def prepareGraph(source, morfo, POS, wgraph, base2vert, sentences):
    src = open(source, 'r')
    num = 0
    for line in src:
        sent = sentence.Sentence(line, num)
        tokens = re.sub('['+string.punctuation+']', ' ', line).lower().split()
        for w in tokens:
            vertBucket = []
            dummy = morfo.lookUpWord(w)
            if 'stopword' in [p for (b, p) in dummy]: continue
            sent.addWord(w)
            related = morfo.getRelated([b for (b, p) in dummy])
            for (base, pos) in dummy:            
                if pos in POS : 
                    if base not in base2vert: base2vert[base] = vertex.WordVertex(base)
                    vertBucket.append(base2vert[base])
            for form in related:
                if form not in base2vert: base2vert[form] = vertex.WordVertex(form)
                vertBucket.append(base2vert[form])
            wgraph.addToWindow(vertBucket)
            wgraph.update()
        sentences.append(sent)
        num += 1
    src.close()

def rankSentences(morfo, POS, sentences, base2vert):
    rank = {}
    denom = 0
    for s in sentences:
        for word in s.getWords():
            dummy = [b for (b, p) in morfo.lookUpWord(word) if p in POS]
            if dummy != []: s.incScore(max([base2vert[base].getScore() for base in dummy]))
        rank[s.getOrdinalNumber()] = s.getScore()
        denom += s.getScore()
    for s in rank: rank[s] /= denom
    return rank
    
def algorithm(source, morfo, POS, w_size, threshold):
    wgraph = graph.GraphOfWords(w_size)
    base2vert = {}
    sentences = []
    prepareGraph(source, morfo, POS, wgraph, base2vert, sentences)    
    #print wgraph.getVertices()
    pr = pageRank.PageRank(wgraph.getVertices(), wgraph.getEdges())
    while not pr.checkConvergence(threshold): pr.pageRankIteration()
    return rankSentences(morfo, POS, sentences, base2vert)
    #return wgraph.getVertices()
    
    
if __name__ == '__main__':
    #morfo = morfeuszDB4GUI.MorfeuszDB4GUI('/home/aglazek/mgr/morfeusz')
    morfo = morfeuszDB4GUI.MorfeuszDB4GUI('/home/aglazek/private/relacje_rozne/word_relations')
    #print algorithm('/home/aglazek/private/teksty/gry_planszowe.txt', morfo, ['noun', 'verb', 'adjective'], 3, 0.01)
    print algorithm('/home/aglazek/private/teksty/konik_polski.txt', morfo, ['noun', 'verb', 'adjective'], 3, 0.01)
