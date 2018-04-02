# textAnalyzer
Objetivo final de analisar o catálogo de disciplinas da UFABC, tanto comparando disciplinas entre si como comparando disciplinas novas que pretendem ser usadas.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Você vai precisar de Python 3 para rodar esta rotina. 

Clone o conteúdo do Github para o seu computador. 
Caso queira comparar a ementa de uma disciplina nova com as existentes no catálogo, edite o arquivo disciplina_nova.csv e coloque as informações (código, ementa, bibliografia, etc) sobre a disciplina nova conforme o nome de cada coluna. Você deve sobrescrever os dados da disciplina de exemplo que consta lá e não colocar uma nova linha. 
Você precisa salvar o arquivo CSV garantindo que é usado o "tab" como separador. 

Em seguida rode o programa:

```
python text analyzer.py
```

Ao final, vc terá uma lista de disciplinas semelhantes, caso existam. 

### Instalação

Simplesmente baixe os arquivo do ramo "master" para um diretório do seu computador. 

Ou ainda, use o git:
```
git close https://github.com/mbreyes/textanalyzer
```

## Authors

* **Marcelo Bussotti Reyes** - *Initial work* - [mbreyes](https://github.com/mbreyes)

## Acknowledgments

* Partes do código deste programa foi retirado de fóruns e discussões sobre python e adaptado. Portanto agradeço à comunidade de forma geral por esta incrível oportunidade de aprendizagem e de troca de ideias. 

