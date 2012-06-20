#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys, urllib, math
import source_document
import rank_method
import random_method, ordinal_method, statistic_method, sentencerank_method, wordrank_method
import agl_morfeusz as morfeusz

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
    
def prepare_automatic_rankings():
    for xt in extractors:
        print '############', xt, '############'
        for tid in texts:
            print texts[tid].getTitle()
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
    
def compare_xtract_method(method, tid, xtract):
    k = len(xtract)
    mres = getTopK(automatic_ranking[(tid, method)], k).keys()
    return len(set(xtract).intersection(set(mres)))*1./k
