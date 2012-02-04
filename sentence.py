#!/usr/bin/python

# Class Sentence -- defines single sentence object, to use as a content of the vertex
import re 
import string

class Sentence(object):
    def __init__(self, orgnl, ordnum):
        self._originalSentence = orgnl
        self._ordinalNumber = ordnum
        self._bow = [] # bag of words
        self._score = 0
        
    def addWord(self, word):
        if word not in self._bow:
            self._bow.append(word)
    
    def getWords(self):
        return self._bow
        
    def getContent(self):
        return self._originalSentence
        
    def getOrdinalNumber(self):
        return self._ordinalNumber
        
    def getOriginalSentence(self):
        return self._originalSentence
        
    def setScore(self, s):
        self._score = s
        
    def incScore(self, x):
        self._score += x*1./len(self._bow)
        
    def getScore(self):
        return self._score

