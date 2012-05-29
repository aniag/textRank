import rank_method
import graph
import vertex
import pageRank

class WordRankMethod(rank_method.RankMethod):

    def _firstPass(self, text):
        for sent in text.getSentences():
            for word in sent.getTokens():
                for base in self.getBases(word):
                    if base not in self._word2vert:
                        self._word2vert[base] = vertex.WordVertex(base)
                        
    def _getConsidered(self, word):
        return set(self.relatedWords(word)).intersection(set(self._word2vert.keys()))

    def _prepareGraph(self, text):
        self._firstPass(text)
        for sent in text.getSentences():
            for word in sent.getTokens():
                vBucket = []
                for form in self._getConsidered(word):
                    vBucket.append(self._word2vert[form])
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
                considered = self._getConsidered(w)
                if len(considered) > 0:
                    rank[sent.getOrdinalNumber()] += max([self._word2vert[word].getScore() for word in considered])*1./len(sent.getTokens())
            denom += rank[sent.getOrdinalNumber()]
        for i in rank: rank[i] /= denom
        return rank
