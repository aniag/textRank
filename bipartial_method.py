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
                (bases, related) = self.relatedWords(word)
                for base in bases:
                    if base not in self._word2vert: 
                        w = vertex.WordVertex(base)
                        self._word2vert[base] = w
                        self._graph.addWordVertex(w)
                    w = self._word2vert[base]
                    v.addNeighbour(w)
                    w.addNeighbour(v)
                for form in related:
                    if form in self._word2Vert:
                        for base in bases:
                            w = self._word2vert[base]
                            w.unionNeighbours(self._word2vert[form].getNeighbours())
                    
                    

    def rankSentences(self, text, threshold=0.01):
        self._graph = graph.BipartialMixedGraph()
        self._word2vert = {}
        self._prepareGraph(text)
        hits = bipartialHITS.BipartialHITS(self._graph._WordVertices, self._graph._SentenceVertices)
        while not hits.checkConvergence(threshold): hits.HITSiteration()
        rank = {}
        denom = 0
        for v in self._graph.getSentenceVertices():
            rank[v.getOrdinalNumber()] = v.getScore()
            denom += v.getScore()
        for i in rank: rank[i] /= denom
        return rank
