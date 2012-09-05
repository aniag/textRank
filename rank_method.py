#!/usr/bin/python
# -*- coding: utf-8 -*-

import stopwords
import related_words
import thesaurus
import math

class RankMethod(object):

    def __init__(self, morfo = None, stopWordsData = None, thesData = None, relData = None, pos = None, d = 0.05):
        self._d = d
        self._use_morfo = False
        self._use_stopwords = False
        self._use_thes = False
        self._use_rel = False
        self._selected_poses = False
        self._stopwords = None
        self._thes = None
        self._rel = None
        if morfo:
            self._morfo = morfo
            self._use_morfo = True
        if stopWordsData:
            self._stopwords = stopwords.StopWords(stopWordsData)
            self._use_stopwords = True
        if thesData:
            self._thes = thesaurus.Thesaurus(thesData)
            self._use_thes = True
        if relData:
            self._rel = related_words.RelatedWords(relData)
            self._use_rel = True
        # makes sens only with morfo=True
        if pos:
            assert self._use_morfo, 'to use POS list, morfo must be enabled'
            self._pos = pos
            self._selected_poses = True
    
    def getBases(self, word):
        bases = []
        if self._use_morfo:
            if self._selected_poses:
                for (base, pos) in self._morfo.getBaseWithPOS(word):
                    if pos in self._pos: bases.append(base)
            else:
                bases = self._morfo.getBasesLists(word)[0]
        if len(bases) == 0 and not self._selected_poses: bases = [word]
        return bases
        
    def getRelatedForms(self, base):
        considered = set()
        if self._use_thes:
            considered.update(set(self._thes.lookUpWord(base)))
        if self._use_rel:
            considered.update(set(self._rel.lookUpWord(base)))
        return considered

    def getWeightedForms(self, word):
        # results = set()
        results = {}
        bases = self.getBases(word)
        base_weight = 1.
        if len(bases) > 0:
            base_weight = 1. / len(bases)
        for base in bases:
            rForms = self.getConsidered(base)
            rForms.discard(base)
            rForm_weight = 0
            if len(rForms) > 0:
                rForm_weight = base_weight / (2*len(rForms))
                base_weight /= 2
            #results.add((base, base_weight))
            results[base] = results.get(base, 0) + base_weight
            for rForm in rForms:
                #results.add((rForm, rForm_weight))
                results[rForm] = results.get(rForm, 0) + rForm_weight
        return set(results.items())

    def relatedWords(self, word):
        considered = set([])
        bases = []
        if self._use_morfo:
            if self._selected_poses:
                for (base, pos) in self._morfo.getBaseWithPOS(word):
                    if pos in self._pos: bases.append(base)
            else:
                bases = self._morfo.getBasesLists(word)[0]
            considered.update(set(bases))
        if self._use_thes:
            if self._use_morfo: 
                for b in bases:
                    considered.update(set(self._thes.lookUpWord(b)))
            else: considered.update(set(self._thes.lookUpWord(word)))
        if self._use_rel:
            if self._use_morfo: 
                for b in bases:
                    considered.update(set(self._rel.lookUpWord(b)))
            else: considered.update(set(self._rel.lookUpWord(word)))
        if len(considered) == 0 and not self._selected_poses: considered = set([word])
        return considered
        
    def printExtract(self, text):
        k = int(math.ceil(len(text.getSentences()) * 1./3))
        ranking = self.rankSentences(text)
        print ranking
        print k
        pairs = ranking.items()
        pairs.sort(key=lambda v: v[1], reverse=True)
        pairs = pairs[:k]
        ranking = dict(pairs)
        tids = ranking.keys()
        tids.sort()
        print tids
        for i in tids:
            print text.getSentence(i).getOriginalSentence()
