
import rank_method

class StatisticMethod(rank_method.RankMethod):

    def relatedWords(self, word):
        considered = set([word])
        if self._use_morfo:
            considered.update(set(self._morfo.getBasesLists(word.encode('utf8'))[0]))
            # print self._morfo.getBasesLists(word.encode('utf8'))[0]
        if self._use_thes:
            considered.update(set(self._thes.lookUpWord(word)))
        if self._use_rel:
            considered.update(set(self._rel.lookUpWord(word)))
        return considered

    def countStats(self, text):
        for sent in text.getSentences():
            for word in sent.getTokens():
                if self._use_stopwords and self._stopwords.isStopWord(word.encode('utf8')): continue
                related = self.relatedWords(word)
                for form in related:
                    if form not in self.words: self.words[form] = 0
                    self.words[form] += 1
    
    def rankSentences(self, text):
        self.words = {}
        self.countStats(text)
        rank = {}
        denom = 0
        for sent in text.getSentences():
            rank[sent.getOrdinalNumber()] = 0
            for word in sent.getTokens():
                if self._use_stopwords and self._stopwords.isStopWord(word.encode('utf8')): continue
                related = self.relatedWords(word)
                rank[sent.getOrdinalNumber()] += max([score for (base, score) in self.words.items() if base in related])*1./len(sent.getTokens())
            denom += rank[sent.getOrdinalNumber()]
        for i in rank: rank[i] /= denom
        return rank
        
