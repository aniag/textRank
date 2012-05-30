
import rank_method

class StatisticMethod(rank_method.RankMethod):

    def _firstPass(self, text):
        for sent in text.getSentences():
            for word in sent.getTokens():
                for base in self.getBases(word):
                    self.words[base] = 0
                                
    def _getConsidered(self, word):
        return set(self.relatedWords(word)).intersection(set(self.words.keys()))

    def countStats(self, text):
        self._firstPass(text)
        for sent in text.getSentences():
            for word in sent.getTokens():
                if self._use_stopwords and self._stopwords.isStopWord(word.encode('utf8')): continue
                for form in self._getConsidered(word):
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
                considered = self._getConsidered(word)
                if len(considered) > 0:
                    rank[sent.getOrdinalNumber()] += max([score for (base, score) in self.words.items() if base in considered])*1./len(sent.getTokens())
            denom += rank[sent.getOrdinalNumber()]
        for i in rank: rank[i] /= denom
        return rank
        
