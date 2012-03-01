import rank_method
import graph
import vertex
import pageRank

class WordRankMethod(rank_method.RankMethod):

    def _prepareGraph(self, text):
        for sent in text.getSentences():
            for word in sent.getTokens():
                vBucket = []
                for form in self.relatedWords(word):
                    if form not in self._word2vert: self._word2vert[form] = vertex.WordVertex(form)
                    vBucket.append(self._word2vert[form])
                if len(vBucket) == 0: continue
                self._graph.addToWindow(vBucket)
                self._graph.update()

    def rankSentences(self, text, wsize = 3, threshold=0.01):
        self._graph = graph.GraphOfWords(wsize)
        self._word2vert = {}
        self._prepareGraph(text)
        pr = pageRank.PageRank(self._graph.getVertices(), self._graph.getEdges())
        while not pr.checkConvergence(threshold): pr.pageRankIteration()
        rank = {}
        denom = 0
        for sent in text.getSentences():
            rank[sent.getOrdinalNumber()] = 0
            for w in sent.getTokens():
                if self._use_stopwords and self._stopwords.isStopWord(word.encode('utf8')): continue
                related = self.relatedWords(w)
                if len(related) > 0:
                    rank[sent.getOrdinalNumber()] += max([self._word2vert[word].getScore() for word in related])*1./len(sent.getTokens())
            denom += rank[sent.getOrdinalNumber()]
        for i in rank: rank[i] /= denom
        return rank
