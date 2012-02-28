
import re
import string
import codecs

class Sentence(object):
    def __init__(self, sent, nb):
        self._originalSentence = sent
        self._ordinalNumber = nb
        self._tokenizedSentence = re.sub('['+string.punctuation+']', ' ', sent).lower().split()
        
class DocumentObject(object):
    def __init__(self, textFile):
        self._sourcePath = textFile
        self._sentences = []
        self.prepare_text()
    
    def prepare_text(self):
        source = codecs.open(self._sourcePath, mode='r', encoding='utf8')
        i = 0
        for line in source:
            if i == 0: self._title = line.strip()
            else: self._sentences.append(Sentence(line.strip(), i-1))
            i += 1
        source.close()
        
    def getTitle(self):
        return self._title
        
    def getSentences(self):
        return self._sentences
    
    def getSentenct(self, nb):
        return self._sentences[nb]
        
