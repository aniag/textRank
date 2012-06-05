#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

class Vertex(object):
    def __init__(self):
        self._score = None
        self._oldScore = 0
        self._neighbours = set()
        self._outSum = 0
    
    def getScore(self):
        return self._score
    
    def getOldScore(self):
        return self._oldScore
        
    def getDiff(self):
        if self._score is None: return float('infinity')
        return abs(self._score - self._oldScore)
    
    def setScore(self, s):
        self._score = s

    def ageScore(self):
        if self._score is not None: self._oldScore = self._score
        
    def setOldScore(self, s):
        self._oldScore = s
    
    def getOutSum(self):
        return self._outSum
    
    def getNeighbours(self):
        return self._neighbours
    
    def addNeighbour(self, v):
        if v not in self._neighbours:
            self._neighbours.add(v)
        
    def incOutSum(self, val):
        self._outSum += val
        
class WordVertex(Vertex):
    def __init__(self, base):
        Vertex.__init__(self)
        self._baseWord = base
        
    def getBaseWord(self):
        return self._baseWord
        
import source_document

class SentenceVertex(Vertex):
    def __init__(self, sent):
        Vertex.__init__(self)
        assert(isinstance(sent, source_document.Sentence))
        self._bow = set([])
        self._sentence = sent
        self._outSum = 0
        
    def getSentence(self):
        return self._sentence
        
    def similarity(self, s):
        try:
            similarity_score = 0
            d1 = dict(self.getAllWords())
            d2 = dict(s.getAllWords())
            for w in d1:
                if w in d2:
                    similarity_score += d1[w] * d2[w]
            similarity_score /= 1. * (math.log(len(self.getAllWords())) + math.log(len(s.getAllWords())))
            return similarity_score
        except (ValueError, ZeroDivisionError):
            return 0
        
    def getAllWords(self):
        return self._bow
            
    def addWords(self, formSet):
        self._bow.update(formSet)
            
    def getOrdinalNumber(self):
        return self._sentence.getOrdinalNumber()
        
    def getOutSum(self):
        return self._outSum
