#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys, urllib, math
import source_document
import rank_method
import random_method, ordinal_method, statistic_method, sentencerank_method, wordrank_method, bipartial_method, even_method
import agl_morfeusz as morfeusz

wikipedia = [2, 3, 5, 7, 8, 9, 11, 13, 18, 20, 22, 24, 30, 31, 32, 33, 34, 35, 37, 39, 40]
polityka = [0, 4, 10, 14, 15, 16, 17, 19, 21, 23, 25, 27]

xtracts = []
single_xtract = {}
complement_ranking = {}
xtract_by_title = {}
average_ranking = {}
texts = {}
extractors = {}
authors = {}
grades = {}
automatic_ranking = {}

familiada_score = {}
rms_error = {}
method_cumulated_error = {}
rms_error_conv = {}
method_cumulated_error_conv = {}
cooccurence_rate = {}
avg_cooccurence_rate = {}
method_token_cmp = {}
pos_diff = {}

def load_texts(filename):
    sources = json.loads(open(filename, 'r').read())
    for tid in sources:
        texts[int(tid)] = source_document.DocumentObject(sources[tid])
    

# z x-tractora ściągana jest lista takich słowników (jeden per ekstrakt):
# {"author": "zg\u0142uch\u0142y malborczyk", "grade": 1, "res": "[0,3,5,8]", "title": "G\u0142azkowo", "datetime": "2012-06-04T12:43:58.009869", "tid": 36}

def load_xtracts(filename):
    source = open(filename, 'r')
    global xtracts 
    xtracts = json.loads(source.read())
    for ex in xtracts:
        ex['res'] = json.loads(ex['res'])
    source.close()

def prepare_single_xtracts():
    for ex in xtracts:
        tid = ex['tid']
        author = ex['author']
        a = authors.get(tid, [])
        a.append(author)
        authors[tid] = a
        x = xtract_by_title.get(tid, [])
        x.append(ex['res'])
        xtract_by_title[tid] = x
        single_xtract[(tid, author)] = ex

def prepare_complement_rankings():
    for ex in xtracts:
        ranking = {}
        denominator = 0
        for coex in xtracts:
            if coex['tid'] == ex['tid'] and coex['author'] != ex['author']:
                for sid in coex['res']:
                    ranking[sid] = ranking.get(sid, 0) + 1.
                    denominator += 1
        for sid in ranking:
            ranking[sid] /= denominator
        complement_ranking[(ex['tid'], ex['author'])] = ranking

def prepare_avg_rankings():
    denominators = {}
    for ex in xtracts:
        tid = ex['tid']
        ranking = average_ranking.get(tid, {})
        for sid in ex['res']:
            ranking[sid] = ranking.get(sid, 0) + 1.
            denominators[tid] = denominators.get(tid, 0) + 1
        average_ranking[tid] = ranking
    for tid in average_ranking:
        ranking = average_ranking[tid]
        for sid in ranking:
            ranking[sid] /= denominators[tid]

def prepare_grades():
    for x in xtracts:
        g = x['grade']
        tid = x['tid']
        if g != None:
            if tid not in grades: grades[tid] = []
            grades[tid].append(g)

def create_extractors(_thesData, _relData, _stopWordsData, _pos):
    # extractors['even'] = even_method.EvenMethod()
    extractors['random'] = random_method.RandomMethod()
    extractors['ordinal'] = ordinal_method.OrdinalMethod()
    extractors['statistic'] = statistic_method.StatisticMethod()
    extractors['statistic+sw'] = statistic_method.StatisticMethod(stopWordsData = _stopWordsData)
    extractors['statistic+morfo+sw'] = statistic_method.StatisticMethod(morfo = morfeusz, stopWordsData = _stopWordsData)
    extractors['statistic+morfo:noun+sw'] = statistic_method.StatisticMethod(morfo = morfeusz, stopWordsData = _stopWordsData, pos = _pos)
    extractors['statistic+morfo+thes+sw'] = statistic_method.StatisticMethod(morfo = morfeusz, thesData = _thesData, stopWordsData = _stopWordsData)
    extractors['statistic+morfo+rel+sw'] = statistic_method.StatisticMethod(morfo = morfeusz, relData = _relData, stopWordsData = _stopWordsData)
    extractors['statistic+morfo+thes+rel+sw'] = statistic_method.StatisticMethod(morfo = morfeusz, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData)
    extractors['statistic+morfo:nouns+thes+rel+sw'] = statistic_method.StatisticMethod(morfo = morfeusz, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData, pos=_pos)
    extractors['wordrank'] = wordrank_method.WordRankMethod()
    extractors['wordrank+sw'] = wordrank_method.WordRankMethod(stopWordsData = _stopWordsData)
    extractors['wordrank+morfo+sw'] = wordrank_method.WordRankMethod(morfo = morfeusz, stopWordsData = _stopWordsData)
    extractors['wordrank+morfo:noun+sw'] = wordrank_method.WordRankMethod(morfo = morfeusz, stopWordsData = _stopWordsData, pos = _pos)
    extractors['wordrank+morfo+thes+sw'] = wordrank_method.WordRankMethod(morfo = morfeusz, thesData = _thesData, stopWordsData = _stopWordsData)
    extractors['wordrank+morfo+rel+sw'] = wordrank_method.WordRankMethod(morfo = morfeusz, relData = _relData, stopWordsData = _stopWordsData)
    extractors['wordrank+morfo+thes+rel+sw'] = wordrank_method.WordRankMethod(morfo = morfeusz, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData)
    extractors['wordrank+morfo:nouns+thes+rel+sw'] = wordrank_method.WordRankMethod(morfo = morfeusz, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData, pos=_pos)
    extractors['sentencerank'] = sentencerank_method.SentenceRankMethod()
    extractors['sentencerank+sw'] = sentencerank_method.SentenceRankMethod(stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo+sw'] = sentencerank_method.SentenceRankMethod(morfo = morfeusz, stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo:noun+sw'] = sentencerank_method.SentenceRankMethod(morfo = morfeusz, stopWordsData = _stopWordsData, pos = _pos)
    extractors['sentencerank+morfo+thes+sw'] = sentencerank_method.SentenceRankMethod(morfo = morfeusz, thesData = _thesData, stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo+rel+sw'] = sentencerank_method.SentenceRankMethod(morfo = morfeusz, relData = _relData, stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo+thes+rel+sw'] = sentencerank_method.SentenceRankMethod(morfo = morfeusz, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData)
    extractors['sentencerank+morfo:nouns+thes+rel+sw'] = sentencerank_method.SentenceRankMethod(morfo = morfeusz, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData, pos=_pos)
    extractors['bipartial'] = bipartial_method.BipartialMethod()
    extractors['bipartial+sw'] = bipartial_method.BipartialMethod(stopWordsData = _stopWordsData)
    extractors['bipartial+morfo+sw'] = bipartial_method.BipartialMethod(morfo = morfeusz, stopWordsData = _stopWordsData)
    extractors['bipartial+morfo:noun+sw'] = bipartial_method.BipartialMethod(morfo = morfeusz, stopWordsData = _stopWordsData, pos = _pos)
    extractors['bipartial+morfo+thes+sw'] = bipartial_method.BipartialMethod(morfo = morfeusz, thesData = _thesData, stopWordsData = _stopWordsData)
    extractors['bipartial+morfo+rel+sw'] = bipartial_method.BipartialMethod(morfo = morfeusz, relData = _relData, stopWordsData = _stopWordsData)
    extractors['bipartial+morfo+thes+rel+sw'] = bipartial_method.BipartialMethod(morfo = morfeusz, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData)
    extractors['bipartial+morfo:nouns+thes+rel+sw'] = bipartial_method.BipartialMethod(morfo = morfeusz, thesData = _thesData, relData = _relData, stopWordsData = _stopWordsData, pos=_pos)
    
def prepare_automatic_rankings():
    for xt in extractors:
        # print '############', xt, '############'
        for tid in texts:
            # print texts[tid].getTitle()
            automatic_ranking[(tid, xt)] = extractors[xt].rankSentences(texts[tid])

def title(tid):
    return texts[tid].getTitle()

def getTopK(ranking, k):
    pairs = ranking.items()
    pairs.sort(key=lambda v: v[1], reverse=True)
    return dict(pairs[:k])
    
def rank_xtract(method, tid, xtract):
    res = 0
    for sid in xtract:
       res += automatic_ranking[(tid, method)].get(sid, 0)
    return res
    
def compare_xtracts_methods():
    for tid, method in automatic_ranking:
        for tid2, token in single_xtract:
            if tid == tid2:
                xtract = single_xtract[(tid2, token)][u'res']
                k = len(xtract)
                mres = getTopK(automatic_ranking[(tid, method)], k).keys()
                method_token_cmp[tid, method, token] =  len(set(xtract).intersection(set(mres)))*1./k

    
def RootMeanSquare(rank1, rank2):
    rms = 0
    sids = set(rank1).union(set(rank2))
    for sid in sids:
        rms += (rank1.get(sid, 0) - rank2.get(sid, 0)) ** 2
    return (rms/len(sids)) ** 0.5

def familiada(ranking, extract):
    res = 0
    for sid in extract:
        res += ranking.get(sid, 0)
    return res

def prepare_rms_errors():
    for ar in automatic_ranking:
        tid, method = ar
        #if tid in [1,4,5,6,7,8,10,11,12,13,14,15,17,19,21,23,24,25,26,27,28]:
        rms = RootMeanSquare(automatic_ranking[ar], average_ranking[tid])
        rms_error[ar] = rms
        method_cumulated_error[method] = method_cumulated_error.get(method, 0) + rms

def CoOccurenceRating(avg_ranking, m_ranking):
    k = int(round(len(m_ranking)/3.))
    pairs = avg_ranking.items()
    pairs.sort(key=lambda v: v[1], reverse=True)
    while(pairs[k-1][1] == pairs[k][1]): k+=1
    avg_res = getTopK(avg_ranking, k).keys()    
    m_res = getTopK(m_ranking, k).keys()
    return len(set(avg_res).intersection(set(m_res)))*1./k

def prepare_conv_rms_errors():
    for ar in automatic_ranking:
        tid, method = ar
        #if tid in [1,4,5,6,7,8,10,11,12,13,14,15,17,19,21,23,24,25,26,27,28]:
        rms = RootMeanSquare(convert_ranking(automatic_ranking[ar]), average_ranking[tid])
        rms_error_conv[ar] = rms
        method_cumulated_error_conv[method] = method_cumulated_error.get(method, 0) + rms


def convert_ranking(ranking):
    p = ranking.items()
    p.sort(key=lambda v : v[1], reverse = True)
    i = 0
    n = len(p)
    res = {}
    for pair in p:
        res[pair[0]] = 2.*(n-i)/(n*(n+1))
        i += 1
    return res

def prepare_coocc_rates():
    for ar in automatic_ranking:
        tid, method = ar
        coocc = CoOccurenceRating(average_ranking[tid], automatic_ranking[ar])
        cooccurence_rate[(tid, method)] = coocc
        x = avg_cooccurence_rate.get(method, [])
        x.append(coocc)
        avg_cooccurence_rate[method] = x
    for method in avg_cooccurence_rate:
        avg_cooccurence_rate[method] = sum(avg_cooccurence_rate[method])/len(avg_cooccurence_rate[method])

def prepare_familiada_scores():
    for ar in automatic_ranking:
        tid, method = ar
        k = int(round(len(automatic_ranking[ar])/3.))
        slist = getTopK(automatic_ranking[ar], k).keys()
        score = familiada(average_ranking[tid], slist)
        familiada_score[ar] = score
    for xt in single_xtract:
        tid, token = xt
        slist = single_xtract[xt][u'res']
        score = familiada(average_ranking[tid], slist)
        familiada_score[xt] = score

def sent_order(ranking):
    p = ranking.items()
    p.sort(key=lambda v : v[1], reverse = True)
    i = 0
    n = len(p)
    res = {}
    for pair in p:
        res[pair[0]] = i
        i += 1
    return res


def prepare_position_diff():
    for ar in automatic_ranking:
        tid, method = ar
        score = 0
        
        pos_diff[ar] = score
