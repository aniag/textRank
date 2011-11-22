#!/usr/bin/python
# -*- coding: utf-8 -*-


import sqlite3

class MorfeuszDB4GUI:

    def __init__(self, path):
        self._dbPath = path
        self._conn = sqlite3.connect(self._dbPath)    
        self._c = self._conn.cursor()
    
    def defaultProgressHandler():
        print '.',
    
    def renewConnection(self):
        self._conn = sqlite3.connect(self._dbPath) 
        self._c = self._conn.cursor()
    
    def load(self, filePath, progress_callback=defaultProgressHandler, force=False):
       
        if not force:
            try: 
                self._c.execute("select '' from morfeusz")
                progress_callback()
                self._c.fetchall()
            except sqlite3.OperationalError:
                force = True
        
        if force:
            self._c.execute('drop table if exists morfeusz ;')
            self._conn.commit()
            progress_callback()
            self._c.execute('''
            create table morfeusz(
            word varchar(60) not null,
            base varchar(60) not null,
            pos varchar(60) not null,
            primary key (word, base, pos));''')
            
            self._conn.commit()
            progress_callback()
            
            print 'Loading morfo-data. May take few minutes...'
            file = open(filePath, 'r')
            i = 0
            for line in file:
                i += 1
                if(i%300 == 0): progress_callback()
                wordList = line.split()
                try: word = wordList[0].decode('utf-8')
                except UnicodeDecodeError: word = wordList[0]
                try: base = wordList[1].decode('utf-8')
                except UnicodeDecodeError: base = wordList[1]
                try: pos = wordList[2].decode('utf-8')
                except UnicodeDecodeError: pos = wordList[2]
                # try:
                self._c.execute('insert into morfeusz(word, base, pos) values(?, ?, ?)', (word, base, pos))
                # except
            self._conn.commit()
            file.close()
            print '..finished!'
            
    def addData(self, filePath):
        print 'Loading morfo-data. May take few minutes...'
        file = open(filePath, 'r')
        i = 0
        for line in file:
            i += 1
            if(i%300 == 0): progress_callback()
            wordList = line.split()
            try: word = wordList[0].decode('utf-8')
            except UnicodeDecodeError: word = wordList[0]
            try: base = wordList[1].decode('utf-8')
            except UnicodeDecodeError: base = wordList[1]
            try: pos = wordList[2].decode('utf-8')
            except UnicodeDecodeError: pos = wordList[2]
            try: self._c.execute('insert into morfeusz(word, base, pos) values(?, ?, ?)', (word, base, pos))
            except sqlite3.IntegrityError: continue
        self._conn.commit()
        file.close()
        print '..finished!'
        
    def isStopWord(self, word):
        try:
            w = word.decode('utf-8')
        except UnicodeEncodeError:
            w = word
        self._c.execute("select pos from morfeusz where word='"+w+"'")
        res = self._c.fetchall()
        #for stopPOS in ['num', 'ppron12', 'ppron3', 'siebie', 'aglt', 'winien', 'prep', 'conj', 'qub']:
        #    if (stopPOS.decode('utf-8'),) in res: return True
        if 'stopword' in res: return True
        return False
        
    def getRelated(self, words):
        if isinstance(words, list):
            w = ''
            for a in words: 
                try:
                    w += "'"+a.decode('utf-8')+"', "
                except UnicodeEncodeError:
                    w += "'"+a+"', "
            w = w[:-2]
        else:
            try:
                w = "'"+words.decode('utf-8')+"'"
            except UnicodeEncodeError:
                w = "'"+words+"'"
        return [x for (x, ) in self._c.execute("select distinct word2 from related where word1 in ("+w+");").fetchall()]
        
    def lookUpWord(self, word):
        try:
            w = word.decode('utf-8')
        except UnicodeEncodeError:
            w = word
        self._c.execute("select base, pos from morfeusz where word='"+w+"'")
        res = self._c.fetchall()
        if len(res) > 0: return res
        # przypadek słowa spoza słownika
        else: return [(w, 'unknown')]

