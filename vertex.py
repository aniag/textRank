#!/usr/bin/python
# -*- coding: utf-8 -*-

class Vertex(object):
    def __init__(self):
        self._score = None
        self._oldScore = 0
        self._neighbours = []
    
    def getScore(self):
        return self._score
    
    def getOldScore(self):
        return self._oldScore
        
    def getDiff(self):
        if self._score is None: return float('infinity')
        return abs(self._score - self._oldScore)
    
    def setScore(self, s):
        if self._score is not None: self._oldScore = self._score
        self._score = s
        
    def setOldScore(self, s):
        self._oldScore = s
    
    def getOutSum(self):
        return len(self._neighbours)
    
    def getNeighbours(self):
        return self._neighbours
    
    def addNeighbour(self, v):
        self._neighbours.append(v)
        
class WordVertex(Vertex):
    def __init__(self, base):
        Vertex.__init__(self)
        self._baseWord = base
        
    def getBaseWord(self):
        return self._baseWord
        
import sentence

class SentenceVertex(Vertex):
    def __init__(self, sent, ordNumb):
        Vertex.__init__(self)
        assert(isinstance(sent, sentence.Sentence))
        self._sentence = sent
        self._ordinalNumber = ordNumb
        self._outSum = 0
        
    def getSentence(self):
        return self._sentence
        
    def getBaseSentence(self):
        return self._sentence._baseSentence
    
    def getOrdinalNumber(self):
        return self._ordinalNumber
        
    def getOutSum(self):
        return self._outSum
        
    def incOutSum(self, val):
        self._outSum += val
