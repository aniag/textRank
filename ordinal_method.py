import rank_method

class OrdinalMethod(rank_method.RankMethod):

    def rankSentences(self, text):
        rank = {}
        n = len(text.getSentences())
        for i in range(n):
            rank[i] = 2.*(n-i)/(n*(n+1))
        return rank
