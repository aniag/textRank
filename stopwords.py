#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs

class StopWords(object):

    def __init__(self, fileName):
        self.setSourceFile(fileName)
        
    def setSourceFile(self, fileName):
        self._sourceFile = fileName
        self._stopwords = []
        
    def _load(self):
        s = codecs.open(self._sourceFile, mode = 'r', encoding='utf8')
        for word in s:
            self._stopwords.append(word.strip())
        
    def isStopWord(self, word):
        '''
        returns True if word is on the stopwords list
        otherwise False
        '''
        if len(self._stopwords) == 0: self._load()
        if not isinstance(word, unicode): word = str(word).decode('utf8')
        if word in self._stopwords: return True
        return False
