import agl_morfeusz
import stopwords
import related_words
import thesaurus

class RankMethod(object):

    def __init__(self, morfo = False, stopWordsData = None, thesData = None, relData = None):
        self._use_morfo = morfo
        self._use_stopwords = False
        self._use_thes = False
        self._use_rel = False
        self._stopwords = None
        self._thes = None
        self._rel = None
        if morfo:
            self._morfo = agl_morfeusz
        if stopWordsData:
            self._stopwords = stopwords.StopWords(stopWordsData)
            self._use_stopwords = True
        if thesData:
            self._thes = thesaurus.Thesaurus(thesData)
            self._use_thes = True
        if relData:
            self._rel = related_words.RelatedWords(relData)
            self._use_rel = True
        
    def relatedWords(self, word):
        considered = set([word])
        if self._use_morfo:
            considered.update(set(self._morfo.getBasesLists(word.encode('utf8'))[0]))
            # print self._morfo.getBasesLists(word.encode('utf8'))[0]
        if self._use_thes:
            if self._use_morfo: 
                for b in self._morfo.getBasesLists(word.encode('utf8'))[0]:
                    considered.update(set(self._thes.lookUpWord(b)))
            else: considered.update(set(self._thes.lookUpWord(word)))
        if self._use_rel:
            if self._use_morfo: 
                for b in self._morfo.getBasesLists(word.encode('utf8'))[0]:
                    considered.update(set(self._rel.lookUpWord(b)))
            else: considered.update(set(self._rel.lookUpWord(word)))
        return considered
