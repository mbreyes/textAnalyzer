#textAnalyzer.py
# -*- coding: utf-8 -*-

from remac import remover_acentos
import string
from stop_words import get_stop_words

#filename = 'catalogo-truncado.txt'
filename = 'catalogo-truncado.txt'


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


# the code below gave problems with utf8
with open(filename, 'r') as myfile:
    #wordstring = myfile.read().replace('\n', '')
    wordstring = myfile.read()

#import codecs
#with codecs.open(filename,'r',encoding='utf8') as f:
#    wordstring = f.read()

# removendo acentuaçao pois temos palavras em português e em inglês - uniformização
wordstring = remover_acentos(wordstring)
# removendo pontos, ponto-e-vírgula, etc
wordstring = wordstring.translate(string.maketrans("",""), string.punctuation)


#import io  
#with io.open(filename,'w',encoding='utf8') as f:
#    f.write(wordstring)
#print wordstring


#wordstring = 'it was the best of times it was the worst of times '
#wordstring += 'it was the age of wisdom it was the age of foolishness'

wordlist = wordstring.split()

wordfreq = []
for w in wordlist:
    wordfreq.append(wordlist.count(w))
    
#allPairs =  str(zip(wordlist, wordfreq)) # náo funcionou porque retorna string
allPairs =  dict(zip(wordlist, wordfreq))
print str(type(allPairs))
allPairs = sortFreqDict(allPairs)

#print "String\n" + wordstring +"\n"
#print "List\n" + str(wordlist) + "\n"
#print "Frequencies\n" + str(wordfreq) + "\n"
print "Pairs\n" + str(allPairs)
