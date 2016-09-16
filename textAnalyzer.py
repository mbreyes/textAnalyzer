
# coding: utf-8

# # Introdução
# 
# O objetivo desse programa é procurar por disciplinas do catálogo da UFABC e identificar disciplinas similares.
# 
# Escrito por: Marcelo Bussotti Reyes - CMCC - UFABC
# Setembro de 2016

# In[1]:

#from remac import remover_acentos
import string
#from stop_words import get_stop_words
import csv
import numpy as np


# Primeiramente obtitve o catálogo de disciplinas em formato excel, gentilmente fornecido pela Prof. Paula Tiba e sua equipe da Pró-Reitoria de Graduação. Exportei para formato csv, colocando como delimitador de campo "tab". O nome do arquivo é 

# In[2]:

filename = 'catalogo2015.csv'
colSigla  = 0                     # coluna que contém as siglas das disciplinas
colNome   = 1                     # coluna com o nome das disciplinas
colEmenta = 4                     # coluna com as ementas
stopWords = ['a'   , 'e' ,  'o' , 'as' , 'os' ,'ao','aos',              'da'  , 'de', 'do' , 'das', 'dos',                         'em'  , 'na', 'no' , 'nos',                                'para','com', 'por', 'à'  , 'às' , 'sobre',                'um'   ,'uma',  'como', 'entre', 'que', 'ou',               '¿'    , ]

ELIM_MOST_FREQ = 50               # além das palavras acima, esta opção permite 
                                  # eliminar palavras mais frequentes presentes nas ementas
ELIM_MULT_OCORRENCIAS = bool(1)      # se True - elimina a contagem múltipla de palavras, contanto somente 1 ocorrência


# Para a identificação das disciplinas, compilamos todas as palavras de cada ementa e colocamos em um dicionário onde a chave é a palavra e o valor é o número de ocorrências da palavra na ementa. 

# In[3]:

def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


# In[4]:

# removendo as palavras muito frequentes como artigos e preposições 
# as stopWords foram definidas no início da rotina
def removeStopWords(texto,stopWords):
    for sw in stopWords:                           # Laço para cada stopWord
        texto = texto.replace(' '+sw+' '," ")      # Remove as stopWords uma a uma. Foram incluídos espaços para evitar 
                                                   # remover partes das palavras
    
    return texto
    


# In[5]:

def limpaTexto(texto,stopWords):
    texto = texto.translate(string.maketrans("",""), string.punctuation)
    texto = texto.lower()
    texto = removeStopWords(texto,stopWords)
    return texto


# In[6]:

def criaVetor(texto):
    palavras = texto.split()                              # quebra a string em uma lista de palavras
    contagemPalavras = []                                 # inicia lista de palavras
    for w in palavras:                                   # loop para cada palavra
        contagemPalavras.append(palavras.count(w))        # conta o número de vezes que cada palavra ocorre na lista
                                                          # e acrescenta à lista contagemPalavras

    vetor =  dict(zip(palavras, contagemPalavras))        # Cria dicionário com as palavras e as respectivas contagens
    return vetor


# In[7]:

catalogo = list(csv.reader(open(filename, 'rb'), delimiter='\t'))


# # Juntando todas as ementas
# 
# Aqui juntamos o texto de todas as ementas e colocamos num único string, para saber todas as palavras usadas

# In[8]:

todasEmentas=''
len(catalogo)
for k in range(1,len(catalogo)):
    todasEmentas = todasEmentas + ' ' + catalogo[k][colEmenta]


# # Removendo stop-words
# Aqui, removemos as pelavras muito frequentes e que não têm a ver com a disciplina em si, mas com a estrutura do português, o que atrapalha no momento de quantificar a sobreposição entre as disciplinas. Usa a função criada no início do código chamada limpaTexto. Abaixo do código, tem um exemplo de texto após a 

# In[9]:

# removendo pontuações e stop-words
todasEmentasLimpo = limpaTexto(todasEmentas,stopWords)


# Abaixo segue um trecho do texto após a remoção das palavras frequentes, pontuação, etc.

# In[10]:

print todasEmentasLimpo[1:1000]


# ## Este passo pode ser bastante demorado
# 
# Nesse ponto temos uma lista (palavras) e uma lista de quantas vezes cada palavra ocorre (contagemPalavras). Vamos agora criar um dicionário com esses pares, e ordená-lo da mais frequente para a menos frequente. 
# 
# !!!Bastante demorado!!!! 
# pode levar até 5 minutos para rodar.

# In[11]:

allPairs  = criaVetor(todasEmentasLimpo)
sortPairs = sortFreqDict(allPairs)                    # usa a função definida no início para ordenar em ordem decrescente


# In[12]:

emptyPairs = {}                                       # inicia variável
for aux in allPairs.keys():                          # loop para todas as palavras
    emptyPairs[aux] = 0                              # cria um dicionário com todas as palavras, mas com contagem zero


# Por curiosidade, vamos visualizar as palavras mais frequentes

# In[13]:

for k in range(50):
    # just for visualization, let's see the mostr frequent words...
    print str(k+1) + ": " + str(sortPairs[k][1]) + ' ==> '+ str(sortPairs[k][0]) + ' vezes'
    


# In[14]:


for k in range(ELIM_MOST_FREQ):
    sortPairs.remove(sortPairs[0])

    
for k in range(50):
    # just for visualization, let's see the mostr frequent words...
    print str(k) + ": " + str(sortPairs[k][1]) + ' ==> '+ str(sortPairs[k][0]) + ' vezes'


# Gerando vetores para palavras frequentes. Aqui, me refiro a vetores, porque são espécies de histogramas indexados pela própria palavra. Python permite esse tipo de estrutura através do tipo "dicionário", ou dict. Assim, é criado um dicionário que contém cada palavra da ementa como chave e o número de ocorrências como entrada. Ex. se a palavra civilização occorre 3 vezes, teremos uma linha do dicionário que será V['civilização']=3, ou {'civilização':3}. As duas maneiras são idênticas para o Python.
# 
# Uma vez criado o vetor de todas as palavras, de todas as ementas, criamos um vetor para cada disciplina, usando como base o vetor geral, de forma que o dicionário de todas as ementas são iguais no número de entradas e nas chaves, somente diferindo no número de ocorrência de cada palavra. 
# 
# Fazendo os vetores idênticos, podemos criar uma matriz "empilhando" os vetores somente do número de entradas. Com isso, criamos uma matriz onde cada linha é o vetor de cada ementa do catálogo. As entradas da matriz V[i,j] são o número de occorrências de palavra[j] na ementa[i], para j indo da primeira à última palavra de todo o catálogo e i indo de 1 até o número de disciplinas.

# In[15]:

V = np.zeros((len(catalogo), len(emptyPairs)),dtype=int)    # inicia o vetor com o tamanho adequado (número de ementas)
l = len(emptyPairs)                                         # guarda o valor do número de palavras total do catálogo
palavras = list()
palavras.append('none')
for k in range(1,len(catalogo)):                           # loop para cada disciplina do catálogo
    estaSigla  = catalogo[k][colSigla ]                     # guarda a sigla da disciplina como uma string
    estaEmenta = catalogo[k][colEmenta]                     # guarda a ementa também como uma única string
        
    estaEmentaLimpa = limpaTexto(estaEmenta,stopWords)      # remove as palavras muito frequêntes como preposições, etc
    palavras.append(estaEmentaLimpa.split())                # cria lista com as palavras menos frequentes de cada ementa
    
    esteVetor = criaVetor(estaEmentaLimpa)                  # cria o vetor com a contagem das palavras para essa disc.
    
    if ELIM_MULT_OCORRENCIAS:
        for p in esteVetor.keys():                          # elimina múltiplas contagens de uma mesma palavra
            if esteVetor[p]>0:                              # deixando o vetor somente com entradas 0 ou 1
                esteVetor[p]=1
    
    vetorCompleto = emptyPairs.copy()                       # cria uma cópia do histograma de todo o catálogo
    vetorCompleto.update(esteVetor)                         # joga as contagens das palavras dessa disciplina no 
                                                            # dicionário geral. Esse passo é necessário para deixar todos
                                                            # os dicionários das disciplinas com o mesmo tamamho e na
                                                            # ordem.
    
    if len(vetorCompleto) != l:                             # Aqui é um pequeno bug. Quando uma ementa começa com uma
                                                            #  palavra frequente, o algoritmo náo consegue remover
                                                            # então preciso fazer essa checagem para uniformizar os vetores
        s1 = set(vetorCompleto.keys())                      # joga todas as palavras dessa disciplina em um conjunto (set)
        s2 = set(allPairs.keys())                           # joga todas as palavras de todas as disciplinas em um set
        s1.difference_update(s2)                            # identifica qual é a palavra diferente guarda em s1
        
        for aux in s1:                                     # for para todas essas palavras
            del vetorCompleto[aux]                          # apaga as entradas do dicionário dessa disciplina 
                
    V[k][:] = np.array(vetorCompleto.values())              # finalmente cria o vetor para essa disciplina e guarda em uma
                                                            # linha da matriz
M = np.inner(V,V)                                           # multiplica a matriz V pela transposta (V'), de forma a obter
                                                            # um produto escalar dos histogramas, que dão uma medida da 
                                                            # da sobreposição entre eles.


# Nesse ponto, temos uma matriz simétrica M[i,j] onde cada entrada é o produto escalar entre a disciplina[i] e a displina[j]. Porém o produto escalar pode variar muito com o tamanho das ementas. Assim, uma medida melhor é dividir o produto escalar pela "norma" de cada disciplina comparada, ou seja, criar um coeficiente coef = M[i,j]/(M[i,i]*M[j,j]), de forma que o coef tenha um valor máximo de 1 (100%) quando as ementas forem idênticas, e zero quando não tiverem qualquer palavra em comum.
# 
# #Ordenando por sobreposição
# Aqui é somente uma preciosidade de ordenar as disciplinas por sobreposição, das mais sobrepostas às menos sobrepostas.

# In[16]:

#lim = int()                               # define um limiar para o módulo dos vetores de palavras das ementas
#(I,J) = (M>lim).nonzero()                  # procura por todos os elementos de matriz cujo valor é superio ao limiar
(I,J) = M.nonzero()

aux = np.array([[I[k],J[k],float(M[I[k],J[k]]*M[I[k],J[k]])/float(M[I[k],I[k]]*M[J[k],J[k]])] for k in range(I.size) ])
#minimo = min(M[I[k],I[k]],M[J[k],J[k]])
#coef2= float(M[I[k],J[k]])/float(minimo)
#aux = np.array([[I[k],J[k],coef2] for k in range(I.size) ])

aux = aux[aux[:,2].argsort(),]

aux = aux[::-1,]                           # coloca o vetor em ordem reversa (de maior sobreposição para menor)

I = aux[0:,0].tolist()                     # converte os índices, agora ordenados para uma lista do python
I = [int(i) for i in I]                   # converte a lista para uma lista de inteiros
J = aux[0:,1].tolist()                     # converte os índicer, agora ordenados para uma lista do python
J = [int(j) for j in J]                   # converte a lista para uma lista de inteiros


# Nesse ponto temos os índices I e J que definem quem das disciplinas que mais se sobrepõem.
# 
# # Gerando lista com ementas em ordem de semelhança
# * Observação:foram eliminadas as disciplinas que contém as palavras: estágio, trabalho, tcc etc (ver código abaixo). Isso é para eliminar as disciplinas como trabalho de graduação

# In[17]:

#print("\033[1;33m texto colorido  \n")
#print '\033[1;31mRed like Radish\033[1;m'
#yellow = '\033[1;33m'
#endYellow = '\033[1;m'
#print(yellow+'bla'+endYellow+'bla')
#i='\033[1;46m'
#f='\033[1;m'
#print 'este texto começa sem cor, mas'+i+'muda'+f+'e depois retorna'




# In[18]:

coef = int();                                              # define o coeficiente como inteiro
for k in range(len(I)):                                   # loop para cada disciplina
#for k in range(10):                                   # loop para cada disciplina
    # --- Calculando o coeficiente de sobreposição ---
    coef = float(M[I[k],J[k]]*M[I[k],J[k]])/float(M[I[k],I[k]]*M[J[k],J[k]])
    minimo = min(M[I[k],I[k]],M[J[k],J[k]]);
    coef2= float(M[I[k],J[k]])/float(minimo)
    nome = catalogo[I[k]][colNome].lower().split()
    
    ementaI = catalogo[I[k]][colEmenta].split()
    ementaJ = catalogo[J[k]][colEmenta].split()
    
    if 0.1 < coef < 2 and I[k] < J[k] and 'graduação' not in set(nome) and          'estágio' not in set(nome) and    'tcc'       not in set(nome): 
        
        print 'Sobreposição = ',int(round(coef*100)),'%\t', 'Sobreposição 2 = ', int(round(coef2*100)),'%'
        print 'Palavras em comum:'
        palavrasComuns = set(palavras[I[k]]).intersection(set(palavras[J[k]]))
        palavrasComuns = list(palavrasComuns)
        
        for i in range(len(palavrasComuns)):
            print palavrasComuns[i],
            
        print '\n'
        print catalogo[I[k]][0],'-', catalogo[I[k]][1], '  --- número', I[k], ' do catálogo'
        print catalogo[I[k]][colEmenta]
        
        #for i in range(len(ementaI)):
        #    if ementaI[i].lower() in palavrasComuns:
        #        #aux='|'+ementaI[i]+'|'
        #        aux=ementaJ[i]
                #aux='\033[1;46m'+ementaI[i]+'\033[1;m]'
        #        print aux,
        #    else:
        #        print ementaI[i],
        print '\n'
        print catalogo[J[k]][0],'-', catalogo[J[k]][1], '  --- número', J[k], ' do catálogo'
        print catalogo[J[k]][colEmenta]
        #for i in range(len(ementaJ)):
        #    if ementaJ[i].lower() in palavrasComuns:
        #        #aux='|'+ementaJ[i]+'|'
        #        aux=ementaJ[i]
        #        print aux,
        #    else:
        #        print ementaJ[i], 
        print '\n','_________________________________________','\n\n'              


# In[19]:

3


# In[ ]:



