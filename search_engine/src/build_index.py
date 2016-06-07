# encoding=utf8

import re
import math

class BuildIndex:

    def __init__(self, text):
        self.text = text
        self.text_to_terms = self.process_text()        
        self.index = self.regIndex()

    def process_text(self):
        text_to_terms = ''  
        pattern = re.compile('[\W_]+')
        text_to_terms = self.text.lower();
        text_to_terms = pattern.sub(' ', text_to_terms)
        re.sub(r'[\W_]+','', text_to_terms)
        text_to_terms = text_to_terms.split()
        return text_to_terms


    def index_text(self, termlist):
        textIndex = {}
        for index, word in enumerate(termlist):
            if word in textIndex.keys():
                textIndex[word].append(index)
            else:
                textIndex[word] = [index]
        return textIndex

    def make_indices(self, termlist):
        return self.index_text(termlist)
 
    def execute(self):
        return self.fullIndex()

    def regIndex(self):
        return self.make_indices(self.text_to_terms)

    def getIndex(self):
        return self.index
