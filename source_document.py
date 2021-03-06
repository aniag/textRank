
import re
import string
import codecs

class Sentence(object):
    def __init__(self, sent, nb):
        self._originalSentence = sent
        self._ordinalNumber = nb
        self._tokenizedSentence = re.sub('['+string.punctuation+']', ' ', sent).lower().split()
    
    def getOriginalSentence(self):
        return self._originalSentence
        
    def getOrdinalNumber(self):
        return self._ordinalNumber
        
    def getTokens(self):
        return self._tokenizedSentence
        
class DocumentObject(object):
    def __init__(self, source):
        self._sentences = []
        if isinstance(source, list):
            self.text_from_list(source)
        else:
            self._sourcePath = source
            self.prepare_text()
        
    def text_from_list(self, source):
        i = 0
        for line in source:
            if i == 0: self._title = line.strip()
            else: self._sentences.append(Sentence(line.strip(), i-1))
            i += 1
    
    def prepare_text(self):
        source = codecs.open(self._sourcePath, mode='r', encoding='utf8')
        i = 0
        self.text_from_list(source)
        source.close()
        
    def getTitle(self):
        return self._title
        
    def getSentences(self):
        return self._sentences
    
    def getSentence(self, nb):
        return self._sentences[nb]
        
