#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, re, operator
import sentence

# Rankingowanie zdań wg popularności (w skali analizowanego tekstu) słów w nim zawartych.


class getByOrderExtract(object):
            
    def __init__(self, mDB, textFile):
        self.sentences = {}
        self.source = textFile
        
    def defaultProgressHandler():
        print '.',
    
    def splitText(self, progress_callback=defaultProgressHandler):
        src = open(self.source)
        i = 0
        for line in src:
            if i%200 == 0: progress_callback()
            self.sentences[i] = sentence.Sentence(line, i)
            i+=1  
        src.close()
    
    def rankSentences(self, progress_callback=defaultProgressHandler):
        rank = {}
        n = len(self.sentences)
        for i in range(n):
            rank[i] = 2.*(n-i)/(n*(n+1))
            self.sentences[i].setScore(rank[i])
        return rank
    
    def getExtract(self, numb):
        sortedVertices = sorted(self.sentences.values(), key=lambda sent: sent.getScore())
        return [ssv.getContent() for ssv in sorted(sortedVertices[-numb:], key=lambda vertex: vertex.getOrdinalNumber())]
        
def doAll(mdb, txt, numb):
    g = getByOrderExtract(mdb, txt)
    g.splitText()
    g.rankSentences()
    for s in g.getExtract(numb): print s
    
if __name__ == '__main__':
    #b = baseLineExtract('/home/aglazek/private/relacje_rozne/word_relations', '/home/aglazek/private/teksty/gry_planszowe.txt')
    g = getByOrderExtract('/home/aglazek/private/relacje_rozne/word_relations', '/home/aglazek/private/teksty/konik_polski.txt')
    g.splitText()
    print ''
    print g.rankSentences()
    
