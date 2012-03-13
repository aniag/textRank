#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib
import math
import source_document
import rank_method
import random_method
import ordinal_method
import statistic_method
import sentencerank_method
import wordrank_method

selections = {}
denominators = {}
importance = {}    
texts = {}
extractors = {}
rankings = {}
distances = {}
avg_dists = {}


def count_importances(url):

    selections = json.loads(urllib.urlopen(url+"results").read())
    for tid in selections:
        denominators[int(tid)] = 0
        for l in selections[tid]:
            denominators[int(tid)] += len(l)
            for s in l: 
                if (int(tid), s) not in importance:
                    importance[(int(tid), s)] = 0
                importance[(int(tid), s)] += 1
              
    #print denominators
    #print importance

#TODO: metody z POSami
def create_extractors(_thesData, _relData, _stopWordsData, _pos):
    extractors['random'] = random_method.RandomMethod()
    extractors['ordinal'] = ordinal_method.OrdinalMethod()
    extractors['statistic'] = statistic_method.StatisticMethod()
    extractors['statistic+sw'] = statistic_method.StatisticMethod(stopWordsData = _stopWordsData)
    extractors['statistic+morfo+sw'] = statistic_method.StatisticMethod(morfo = True, stopWordsData = _stopWordsData)
    extractors['statistic+morfo:noun+sw'] = statistic_method.StatisticMethod(morfo = True, stopWordsData = _stopWordsData, pos = _pos)
    extractors['statistic+morfo+thes+sw'] = statistic_method.StatisticMethod(morfo = True, thesData = _thesData, stopWordsData = _stopWordsData)
    extractors['statistic+morfo+rel+sw'] = statistic_method.StatisticMethod(morfo = True, relData = _relData, stopWordsData = _stopWordsData)
    extractors['statistic+morfo+thes+rel+sw'] = statistic_method.StatisticMethod(morfo = True, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData)
    extractors['statistic+morfo:nouns+thes+rel+sw'] = statistic_method.StatisticMethod(morfo = True, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData, pos=_pos)
    extractors['wordrank'] = wordrank_method.WordRankMethod()
    extractors['wordrank+sw'] = wordrank_method.WordRankMethod(stopWordsData = _stopWordsData)
    extractors['wordrank+morfo+sw'] = wordrank_method.WordRankMethod(morfo = True, stopWordsData = _stopWordsData)
    extractors['wordrank+morfo:noun+sw'] = wordrank_method.WordRankMethod(morfo = True, stopWordsData = _stopWordsData, pos = _pos)
    extractors['wordrank+morfo+thes+sw'] = wordrank_method.WordRankMethod(morfo = True, thesData = _thesData, stopWordsData = _stopWordsData)
    extractors['wordrank+morfo+rel+sw'] = wordrank_method.WordRankMethod(morfo = True, relData = _relData, stopWordsData = _stopWordsData)
    extractors['wordrank+morfo+thes+rel+sw'] = wordrank_method.WordRankMethod(morfo = True, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData)
    extractors['wordrank+morfo:nouns+thes+rel+sw'] = wordrank_method.WordRankMethod(morfo = True, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData, pos=_pos)
    extractors['sentencerank'] = sentencerank_method.SentenceRankMethod()
    extractors['sentencerank+sw'] = sentencerank_method.SentenceRankMethod(stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo+sw'] = sentencerank_method.SentenceRankMethod(morfo = True, stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo:noun+sw'] = sentencerank_method.SentenceRankMethod(morfo = True, stopWordsData = _stopWordsData, pos = _pos)
    extractors['sentencerank+morfo+thes+sw'] = sentencerank_method.SentenceRankMethod(morfo = True, thesData = _thesData, stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo+rel+sw'] = sentencerank_method.SentenceRankMethod(morfo = True, relData = _relData, stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo+thes+rel+sw'] = sentencerank_method.SentenceRankMethod(morfo = True, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo:nouns+thes+rel+sw'] = sentencerank_method.SentenceRankMethod(morfo = True, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData, pos=_pos)
    

def load_texts(url):
    sources = json.loads(urllib.urlopen(url+'sources').read())
    for tid in sources:
        texts[int(tid)] = source_document.DocumentObject(sources[tid])
    

def count_ref_ranking_for_text(text_id):
    rank = {}
    for (tid, s) in importance:
        if tid == text_id:
            rank[s] = importance[(tid, s)]*1./denominators[tid]
    return rank


def compareExtracts(xt_method, tid):
    r = rankings[(tid, xt_method)]
    ref = rankings[(tid, 'x-tractor')]
    r_ext = map(lambda (x,y):x, sorted(r.items(), key = lambda (x, y): -y)[:int(math.ceil(len(r)/3))])
    ref_ext = map(lambda (x,y):x, sorted(ref.items(), key = lambda (x, y): -y)[:int(math.ceil(len(r)/3))])
    return len(set(r_ext).intersection(set(ref_ext))) *1./len(ref_ext)

def prepareStatistics():
    for tid in texts:
        ln = len(texts[tid].getSentences())
        rankings[(tid, 'x-tractor')] = count_ref_ranking_for_text(tid)
        for xt in extractors:
            print tid, xt
            dist = 0
            rankings[(tid, xt)] = extractors[xt].rankSentences(texts[tid])
            for i in range(ln):
                if i not in rankings[(tid, xt)]: a = 0
                else: a = rankings[(tid, xt)][i]
                if i not in rankings[(tid, 'x-tractor')]: b = 0
                else: b = rankings[(tid, 'x-tractor')][i]
                dist += pow((a-b), 2)
            distances[(tid, xt)]= math.sqrt(dist)
    for xt in extractors:
        d = [distances[(tid, xt)] for tid in texts]
        avg_dists[xt] = sum(d)/len(d)

if __name__ == '__main__':
    count_importances('http://localhost:9999/main/')
    load_texts('http://localhost:9999/main/')
    create_extractors('/home/aglazek/private/praca/lang_data/thesaurus-utf8.txt', '/home/aglazek/private/praca/lang_data/related_words.txt', '/home/aglazek/private/praca/lang_data/combined_stopwords.txt', ['noun'])
    prepareStatistics()
    print rankings
    print distances
    print avg_dists
