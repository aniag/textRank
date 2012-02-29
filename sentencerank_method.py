import rank_method
import graph
import vertex
import pageRank

class SentenceRankMethod(rank_method.RankMethod):

    def _prepareGraph(self, text):
        for sent in text.getSentences():
            v = vertex.SentenceVertex(sent)
            for word in sent.getTokens():
                v.addWords(self.relatedWords(word))            
            self._graph.update(v)

    def rankSentences(self, text, threshold=0.01):
        self._graph = graph.GraphOfSentences()
        self._prepareGraph(text)
        pr = pageRank.PageRank(self._graph.getVertices(), self._graph.getEdges())
        while not pr.checkConvergence(threshold): pr.pageRankIteration()
        rank = {}
        denom = 0
        for v in self._graph.getVertices():
            rank[v.getOrdinalNumber()] = v.getScore()
        for i in rank: rank[i] /= sum(rank.values())
        return rank
