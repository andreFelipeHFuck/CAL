import numpy as np
import random

from datetime import datetime

num_cidades = 3

list_nome = np.array(['Joinville', 'Florianopolis', 'Tubarao'])

dict_nome = {n:v for n,v in zip(list_nome, [i for i in range(len(list_nome))])}

distancia_cidades = np.array([
                             [0, 10, 20],
                             [10, 0, 1000],
                             [20, 1000, 0]
                             ])

def distancia_entre_cidades(a:int, b:int) -> int:
    return distancia_cidades[a][b]

def distancia_entre_cidades_nome(cidadeA: str, cidadeB: str)->int:
    return distancia_entre_cidades(dict_nome[cidadeA], dict_nome[cidadeB])

def cria_primeira_populacao(lista_cidades, num_populacao)->list:
    
    populacao_set = []

    for _ in range(num_populacao):
        sol_i = lista_cidades[np.random.choice(list(range(num_cidades)), num_cidades, replace=False)]
        populacao_set.append(sol_i)
    return np.array(populacao_set)

populacao_set = cria_primeira_populacao(list_nome, 10)

def valor_fitness(lista_cidades)->int:
    total = 0
    for i in range(num_cidades - 1):
        cidadeA = lista_cidades[i]
        cidadeB = lista_cidades[i + 1]
        total += distancia_entre_cidades_nome(cidadeA, cidadeB)
    return total


def get_todas_fitness(populacao_set, num_populacao):
    list_fitness = np.zeros(num_populacao)

    for i in range(num_populacao):
        list_fitness[i] = valor_fitness(populacao_set[i])

    return list_fitness

list_fitness = get_todas_fitness(populacao_set, 10)

def selecao_progenitores(populacao_set, list_fitness):
      total_fit = list_fitness.sum()
      prob_list = list_fitness/total_fit
    
      #Notice there is the chance that a progenitor. mates with oneself
      progenitor_list_a = np.random.choice(list(range(len(populacao_set))), len(populacao_set),p=prob_list, replace=True)
      progenitor_list_b = np.random.choice(list(range(len(populacao_set))), len(populacao_set),p=prob_list, replace=True)
        
      progenitor_list_a = populacao_set[progenitor_list_a]
      progenitor_list_b = populacao_set[progenitor_list_b]
    
    
      return np.array([progenitor_list_a,progenitor_list_b])


list_progenistores = selecao_progenitores(populacao_set, list_fitness)
print(list_progenistores[0][2])

