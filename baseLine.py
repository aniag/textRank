#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, re, operator
import morfeuszDB4GUI
import sentence

# Rankingowanie zdań wg popularności (w skali analizowanego tekstu) słów w nim zawartych.


class baseLineExtract(object):
            
    def __init__(self, mDB, textFile):
        self.words = {}
        self.sentences = {}
        self.source = textFile
        self.morfo = morfeuszDB4GUI.MorfeuszDB4GUI(mDB)
        
    def defaultProgressHandler():
        print '.',
    
    def countStats(self, progress_callback=defaultProgressHandler):
        src = open(self.source)
        i = 0
        for line in src:
            if i%200 == 0: progress_callback()
            tokens = re.sub('['+string.punctuation+']', ' ', line).lower().split()
            self.sentences[i] = sentence.Sentence(line, i)
            for word in tokens:
                dummy = self.morfo.lookUpWord(word)
                if 'stopword' in [p for (b, p) in dummy]: continue
                self.sentences[i].addWord(word) 
                for (base, pos) in dummy:
                    if base not in self.words:
                        self.words[base] = 0
                    self.words[base] += 1  
            i+=1  
        src.close()
                
    def getTopWords(self, param):
        return sorted(self.words.iteritems(), key=operator.itemgetter(1))[-param:]
    
    def rankSentences(self, progress_callback=defaultProgressHandler):
        rank = {}
        denom = 0
        for s in self.sentences.values():
            for word in s.getWords():
                dummy = [b for (b, p) in self.morfo.lookUpWord(word)]
                s.incScore(max([score for (base, score) in self.words.items() if base in dummy]))
            rank[s.getOrdinalNumber()] = s.getScore()
            denom += s.getScore()
        for s in rank: rank[s] /= denom
        return rank
    
    def getExtract(self, numb):
        sortedVertices = sorted(self.sentences.values(), key=lambda sent: sent.getScore())
        return [ssv.getContent() for ssv in sorted(sortedVertices[-numb:], key=lambda vertex: vertex.getOrdinalNumber())]
        
def doAll(mdb, txt, numb):
    b = baseLineExtract(mdb, txt)
    b.countStats()
    b.rankSentences()
    for s in b.getExtract(numb): print s
    
if __name__ == '__main__':
    b = baseLineExtract('/home/aglazek/mgr/morfeusz', '/home/aglazek/private/teksty/czekan.txt')
    b.countStats()
    print ''
    print b.rankSentences()
    
