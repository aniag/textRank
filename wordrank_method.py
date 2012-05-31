import rank_method
import graph
import vertex
import pageRank

class WordRankMethod(rank_method.RankMethod):

    def _prepareGraph(self, text):
        for sent in text.getSentences():
            for word in sent.getTokens():
                vBucket = []
                bases = self.getBases(word)
                for base in bases:
                    if base not in self._word2vert: self._word2vert[base] = vertex.WordVertex(base)
                    vBucket.append(self._word2vert[base])
                    for form in self.getRelated(base):
                        try:
                            w = self._word2vert[base]
                            v = self._word2vert[form]
                            self._graph.addEdge(w, v, 0.1)
                        except KeyError:
                            pass
                if len(vBucket) == 0: continue
                self._graph.addToWindow(vBucket)
                self._graph.update()

    def rankSentences(self, text, wsize = 3, threshold=0.0001):
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
                if self._use_stopwords and self._stopwords.isStopWord(w.encode('utf8')): continue
                related = self.getBases(w)
                if len(related) > 0:
                    rank[sent.getOrdinalNumber()] += max([self._word2vert[word].getScore() for word in related])*1./len(sent.getTokens())
            denom += rank[sent.getOrdinalNumber()]
        for i in rank: rank[i] /= denom
        return rank
