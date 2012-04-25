import rank_method
import graph
import vertex
import pageRank

class BipartialMethod(rank_method.RankMethod):

    def _prepareGraph(self, text):
        for sent in text.getSentences():
            v = vertex.SentenceVertex(sent)
            self._graph.addVertex(v)
            for word in sent.getTokens():
                for form in self.relatedWords(word):
                    if form not in self._word2vert: 
                        w = vertex.WordVertex(form)
                        self._word2vert[form] = w
                        self._graph.addVertex(w)
                    self._graph.addEdge(v, w, 1)
                    v.addNeighbour(w)
                    w.addNeighbour(v)
                    w.incOutSum(1)
                    v.incOutSum(1)
                    
                    

    def rankSentences(self, text, threshold=0.01):
        self._graph = graph.Graph()
        self._word2vert = {}
        self._prepareGraph(text)
        pr = pageRank.PageRank(self._graph.getVertices(), self._graph.getEdges(), 0)
        while not pr.checkConvergence(threshold): pr.pageRankIteration()
        rank = {}
        denom = 0
        for v in self._graph.getVertices():
            if type(v) == vertex.SentenceVertex:
                rank[v.getOrdinalNumber()] = v.getScore()
                denom += v.getScore()
        for i in rank: rank[i] /= denom
        return rank
