#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs


class RelatedWords(object):

    def __init__(self, sourceFile):
        self._sourceFile = sourceFile
        self._index = {}
        self._inverted = {}

    def _union(self, i, j):
        (new, old) = (i, j) if i < j else (j, i)
        toChange = self._inverted.pop(old)
        for w in toChange:
            self._index[w] = new
            self._inverted[new].append(w)
                

    def prepare_representation(self):
        '''
        prepares dictionary with strings as keys and integers as values
        value stores an index of the synset for the word being its key
        '''
        print '[INFO] preparing structure'
        i = 0
        source = codecs.open(self._sourceFile, mode='r', encoding='utf8')
        for line in source:
            [x, y] = line.strip().split(' ')
            if x in self._index and y in self._index and self._index[x] != self._index[y]:
                self._union(self._index[x], self._index[y])
            if x not in self._index and y not in self._index:
                self._inverted[i] = [x, y]
                self._index[x] = i
                self._index[y] = i
                i += 1
            elif x not in self._index:
                self._index[x] = self._index[y]
                self._inverted[self._index[y]].append(x)
            elif y not in self._index:
                self._index[y] = self._index[x]
                self._inverted[self._index[x]].append(y)
        source.close()
        print '[INFO] preprocessing finnished'

    def lookUpWord(self, word):
        '''
        returns list of related words if word was founded in index
        given word otherwise
        '''        
        res = []
        if len(self._index) == 0: self.prepare_representation()
        if not isinstance(word, unicode): word = str(word).decode('utf8')
        try:
            idx = self._index[word]
        except KeyError:
            return [word]
        '''
        for t in self._index:
            if self._index[t] == idx:
                res.append(t)
        return res
        '''
        return self._inverted[idx]
