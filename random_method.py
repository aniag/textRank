import rank_method
import random

class RandomMethod(rank_method.RankMethod):

    def rankSentences(self, text):
        rank = {}
        n = len(text.getSentences())
        for i in range(n):
            rank[i] = 2.*(n-i)/(n*(n+1))
        random.shuffle(rank)
        return rank
