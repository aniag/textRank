#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import sentence
import morfeuszDB4GUI
import operator
import pageRank
import vertex

def similarity(s, t):
    return len([w for w in s.getWords() if w in t.getWords()]) * 1. / (math.log(len(s.getWords())) + math.log(len(t.getWords())))

def prepareGraph(source, morfo, POS):
    vertices = []
    edges = {}
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
        for w in vertices:
            # edges[(v, w)] = edges[(w, v)] = similarity(sent, w.getSentence())
            edges[(v, w)] = edges[(w, v)] = len([w for w in sent.getWords() if w in w.getSentence().getWords()]) * 1. / (math.log(len(sent.getWords())) + math.log(len(w.getSentence().getWords())))
        vertices.append(v)
        num += 1
    src.close()
    return (vertices, edges)

def algorithm(source, morfo, POS, threshold):
    pr = pageRank.PageRank(prepareGraph(source, morfo, POS))
    while not pr.checkConvergence(threshold): pr.pageRankIteration()
    
    
def main():
    

if __name__ == '__main__':
    main()    
