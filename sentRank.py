#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import sentence
import morfeuszDB4GUI
import operator
import pageRank
import vertex

def prepareGraph(source, morfo, POS):
    vertices = []
    edges = {}
    src = open(source, 'r')
    num = 0
    for line in src:
        sent = sentence.Sentence(line, num)
        v = vertex.WordVertex(sent, num)
        tokens = re.sub('['+string.punctuation+']', ' ', line).lower().split()
        for w in tokens:
            dummy = morfo.lookUpWord(w)
            if 'stopword' in [p for (b, p) in dummy]: continue
            for (base, pos) in dummy:
                if pos in POS : sent.addWord(base)
        num += 1
    src.close()

def algorithm(source, morfo, POS):
        
def main():
    

if __name__ == '__main__':
    main()    
