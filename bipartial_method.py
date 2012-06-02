import rank_method
import graph
import vertex
import bipartialHITS

class BipartialMethod(rank_method.RankMethod):

    def _firstPass(self, text):
        for sent in text.getSentences():
            for word in sent.getTokens():
                for base in self.getBases(word):
                    if base not in self._word2vert:
                        w = vertex.WordVertex(base)
                        self._word2vert[base] = w
                        self._graph.addWordVertex(w)
                        
    def _getConsidered(self, word):
        return set(self.relatedWords(word)).intersection(set(self._word2vert.keys()))

    def _prepareGraph(self, text):
        self._firstPass(text)
        for sent in text.getSentences():
            v = vertex.SentenceVertex(sent)
            self._graph.addSentenceVertex(v)
            for word in sent.getTokens():
                for form in self._getConsidered(word):
                    w = self._word2vert[form]
                    self._graph.addEdge(v, w, 1)
                    
                    

    def rankSentences(self, text, threshold=0.0001):
        self._graph = graph.BipartialMixedGraph()
        self._word2vert = {}
        self._prepareGraph(text)
        hits = bipartialHITS.BipartialHITS(self._graph._WordVertices, self._graph._SentenceVertices, self._graph._edges)
        hits.HITSiteration()
        while not hits.checkConvergence(threshold): hits.HITSiteration()
        rank = {}
        denom = 0
        for v in self._graph.getSentenceVertices():
            rank[v.getOrdinalNumber()] = v.getScore()
            denom += v.getScore()
        for i in rank: rank[i] /= denom
        return rank
