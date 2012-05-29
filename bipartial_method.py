import rank_method
import graph
import vertex
import bipartialHITS

class BipartialMethod(rank_method.RankMethod):

    def _prepareGraph(self, text):
        for sent in text.getSentences():
            v = vertex.SentenceVertex(sent)
            self._graph.addSentenceVertex(v)
            for word in sent.getTokens():
                for form in self.relatedWords(word):
                    if form not in self._word2vert: 
                        w = vertex.WordVertex(form)
                        self._word2vert[form] = w
                        self._graph.addWordVertex(w)
                    w = self._word2vert[form]
                    self._graph.addEdge(v, w, 1)
                    v.addNeighbour(w)
                    w.addNeighbour(v)
                    
                    

    def rankSentences(self, text, threshold=0.0001):
        self._graph = graph.BipartialMixedGraph()
        self._word2vert = {}
        self._prepareGraph(text)
        hits = bipartialHITS.BipartialHITS(self._graph._WordVertices, self._graph._SentenceVertices, self._graph.getEdges())
        while not hits.checkConvergence(threshold): hits.HITSiteration()
        rank = {}
        denom = 0
        for v in self._graph.getSentenceVertices():
            rank[v.getOrdinalNumber()] = v.getScore()
            denom += v.getScore()
        for i in rank: rank[i] /= denom
        return rank
