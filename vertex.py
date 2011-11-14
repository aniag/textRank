#!/usr/bin/python
# -*- coding: utf-8 -*-

class Vertex:
    def __init__(self):
        self._score = 0
        self._oldScore = float('infinity')
        self._neighbours = []
    
    def getScore(self):
        return self._score
    
    def getOldScore(self):
        return self._oldScore
        
    def getDiff(self):
        return abs(self._score - self._oldScore)
    
    def setScore(self, s):
        self._oldScore = self._score
        self._score = s
    
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
        
    def getSentence(self):
        return self._sentence
        
    def getBaseSentence(self):
        return self._sentence._baseSentence
    
    def getOrdinalNumber(self):
        return self._ordinalNumber
