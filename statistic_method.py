
import rank_method

class StatisticMethod(rank_method.RankMethod):

    def check(self):
        if self._use_morfo: print 'using morfo' 
