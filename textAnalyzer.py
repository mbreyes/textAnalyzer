
# coding: utf-8

# # Introduction
# This is my first python notebook.
# It seems that I can use latex stuff in here.
# 
# The stop-words module was installed from: https://pypi.python.org/pypi/stop-words#installation
# and using the command: pip install stop-words 
# 

# In[1]:

from remac import remover_acentos
import string
from stop_words import get_stop_words


# Primeiramente criei um catálogo truncado de disciplinas para fazer os primeiros testes de forma mais rápida. 

# In[2]:

filename = 'catalogo-truncado.txt'


# Criando uma função para colocar o dicionário em ordem alfabética.

# In[3]:

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


# Um dos problemas em lidar com textos em português são os acentos. Mas usando utf-8 tudo deveria ficar bem. Eu fiz dois testes, e esse primeiro deu uns problemas com o utf8...

# In[5]:

# the code below gave problems with utf8
with open(filename, 'r') as myfile:
    #wordstring = myfile.read().replace('\n', '')
    wordstring = myfile.read()


# Supostamente o código abaixo funcionou melhor, mas por algum motivo foi abandonado. Vou deixar aqui para uso futuro.

# In[6]:

#import codecs
#with codecs.open(filename,'r',encoding='utf8') as f:
#    wordstring = f.read()


# Lembro que uma das alternativas que eu havia pensado era remover os acentos. Mas acho que isso se deu por problemas em usar o utf8.

# In[7]:

# removendo acentuaçao pois temos palavras em português e em inglês - uniformização
wordstring = remover_acentos(wordstring)


# In[8]:

# removendo pontos, ponto-e-vírgula, etc
wordstring = wordstring.translate(string.maketrans("",""), string.punctuation)


# In[9]:

#import io  
#with io.open(filename,'w',encoding='utf8') as f:
#    f.write(wordstring)
#print wordstring


# In[10]:

#wordstring = 'it was the best of times it was the worst of times '
#wordstring += 'it was the age of wisdom it was the age of foolishness'


# In[11]:

wordlist = wordstring.split()
wordfreq = []
for w in wordlist:
    wordfreq.append(wordlist.count(w))


# In[23]:

#allPairs =  str(zip(wordlist, wordfreq)) # náo funcionou porque retorna string
allPairs =  dict(zip(wordlist, wordfreq))
print str(type(allPairs)) # só imprime na tela o tipo de variável
allPairs = sortFreqDict(allPairs)

for k in range(10):
    mostFreq = allPairs[k];
    mostFreq = mostFreq[1];
    print str(k) + " ==> " + str(mostFreq)

#myAllPairs = mySortFreqDict(allPairs)
#allPairs = [(allPairs[key], key) for key in allPairs]
#print str(type(allPairs))
#allPairs.size
#print allPairs[0:2][0:2]
#aux = zip(allPairs[0:10])

#print aux.index("de")

#print aux
#my_dict = {'x':1, 'y':2, 'z':3}
#dict((value, key) for key, value in my_dict.iteritems())
#my_dict.iteritems()



#l = ['a',' b',' c',' d',' e']
#c_index = l.index(" c")
#l2 = l[:c_index]
#print l2


# In[ ]:

#print "String\n" + wordstring +"\n"
#print "List\n" + str(wordlist) + "\n"
#print "Frequencies\n" + str(wordfreq) + "\n"
print "Pairs\n" + str(allPairs)


# In[ ]:




# In[ ]:



