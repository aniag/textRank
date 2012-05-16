#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs


class Thesaurus(object):

    def __init__(self, thesFile):
        self._thesFile = thesFile
        self._thes = {}
        self._inverted = {}

    def prepare_representation(self):
        '''
        prepares dictionary with strings as keys and lists of integers as values
        value stores a list of synset indexes for the word being its key
        '''
        print '[INFO] preparing structure'
        i = 0
        source = codecs.open(self._thesFile, mode='r', encoding='utf8')
        for line in source:
            self._inverted[i] = []
            entries = line.strip().split(';')
            for entry in entries:
                self._inverted[i].append(entry)
                if entry not in self._thes:
                    self._thes[entry] = []
                self._thes[entry].append(i)
                
            i += 1
        source.close()
        print '[INFO] preprocessing finnished'

    def lookUpWord(self, word):
        '''
        returns list of synonyms if word was founded in thesaurus
        given word otherwise
        '''        
        res = []
        if len(self._thes) == 0: self.prepare_representation()
        if not isinstance(word, unicode): word = str(word).decode('utf8')
        try:
            idxs = self._thes[word]
        except KeyError:
            return [word]
        '''
        for t in self._thes:
            if self._thes[t][0] > max(idxs): continue
            if self._thes[t][-1] < min(idxs): continue
            if len(set(self._thes[t]).intersection(set(idxs))) > 0:
                res.append(t)
        '''
        for i in idxs:
            res += self._inverted[i]
        return res
        
