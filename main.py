import numpy as np
import random

from datetime import datetime

num_cidades = 3
taxa_mutacao = 0.3

list_nome = np.array(["Joinville","Florianópolis","Blumenau","São José","Lages","Criciúma","Chapecó","Itajaí","Jaraguá do Sul","Brusque","Tubarão","Balneário Camboriú","Santa Catarina","São Bento do Sul","Caçador"])

dict_nome = {n:v for n,v in zip(list_nome, [i for i in range(len(list_nome))])}

distancia_cidades = np.array([
                             [0,177,98,173,307,357,513,89,50,115,298,98,311,77,328],
                             [176, 0,140,10,223,195,550,92,188,100,136,81,227,240,401],
                             [94,142, 0,139,224,322,478,53,65,40,263,63,228,120,307],
                             [173,10,136,0,214,187,540,88,184,96,128,78,218,236,391],
                             [304,224,223,214,0,200,331,271,260,262,213,281,4,307,185],
                             [357,197,321,187,200, 0,529,272,368,280,61,262,203,420,380],
                             [513,551,477,541,330,529,0,585,487,585,542,594,332,443,220],
                             [89,96,53,92,272,276,585, 0,100,34,217,12,276,152,400],
                             [45,186,65,183,257,366,488,99,0,98,307,108,261,55,302],
                             [116,102,40,98,261,282,585,36,97,0,223,43,265,152,344],
                             [296,136,260,126,213,61,542,211,308,220,0,201,217,360,393],
                             [99,82,63,79,290,262,595,11,110,43,203,0,294,162,409],
                             [307,228,227,218,4,204,332,275,264,265,217,285,0,310,188],
                             [80,240,119,236,304,420,441,152,55,152,361,161,308,0,255],
                             [328,402,307,392,185,380,220,400,302,345,393,409,188,258,0]
                             ])

class Cidades:
    def __init__(self, nome_cidades: list, distancia_cidades: list, num_populacao: int, taxa_mutacao: float) -> None:
        self.nome_cidades = nome_cidades
        self.distancia_cidades = distancia_cidades

        self.dict_cidades = {c:v for c,v in zip(nome_cidades, [i for i in range(len(nome_cidades))])}
        self.num_cidades = len(nome_cidades)

        self.num_populacao = num_populacao
        self.taxa_mutacao = taxa_mutacao

        self.populacao_set = self.primeira_populacao()
        self.list_fitness = self.get_todas_fitness()
        self.list_progenitores = self.selecao_progenitores()
        self.nova_populacao_set = self.gera_populacao()
        self.populacao_mutada = self.mutacao_populacao()

        self.melhor_solucao = []

    def distancia_entre_cidades(self, a: int, b: int) -> int:
        return self.distancia_cidades[a][b]
    
    def distancia_entre_cidades_nome(self, cidadeA: str, cidadeB: str) -> int:
        return self.distancia_entre_cidades(self.dict_cidades[cidadeA], self.dict_cidades[cidadeB])
    
    def primeira_populacao(self) -> list:
        populaca_set = []

        # Gera as primeiras soluções
        for _ in range(self.num_populacao):
            sol_i = self.nome_cidades[np.random.choice(list(range(self.num_cidades)), self.num_cidades, replace=False)]
            populaca_set.append(sol_i)

        return np.array(populaca_set)
    
    def valor_fitness(self, lista_cidades) -> int:
        total = 0
        for i in range(self.num_cidades - 1):
            cidadeA = lista_cidades[i]
            cidadeB = lista_cidades[i + 1]
            total += self.distancia_entre_cidades_nome(cidadeA, cidadeB)

        return total

    def get_todas_fitness(self) -> list:
        list_fitness = np.zeros(self.num_populacao)

        for i in range(self.num_populacao):
            list_fitness[i] = self.valor_fitness(self.populacao_set[i])

        return list_fitness
    
    def selecao_progenitores(self) -> list:
        total_fit = self.list_fitness.sum()
        prob_list = self.list_fitness/total_fit

        progenitor_list_a = np.random.choice(list(range(len(self.populacao_set))), len(self.populacao_set), p=prob_list ,replace=True)
        progenitor_list_b = np.random.choice(list(range(len(self.populacao_set))), len(self.populacao_set), p=prob_list, replace=True)

        progenitor_list_a = self.populacao_set[progenitor_list_a]
        progenitor_list_b = self.populacao_set[progenitor_list_b]

        return np.array([progenitor_list_a, progenitor_list_b])
    

    def gera_filho(self, progenitorA, progenitorB) -> list:
        filho = progenitorA[0:1]

        for cidade in progenitorB:
            if not cidade in filho:
                filho = np.concatenate((filho, [cidade]))
        
        return filho
    
    def gera_populacao(self) -> list:
        nova_populacao_set = []

        for i in range(self.list_progenitores.shape[1]):
            progenitorA, progenitorB = self.list_progenitores[0][i], self.list_progenitores[1][i]
            filho = self.gera_filho(progenitorA, progenitorB)
            nova_populacao_set.append(filho)

        return nova_populacao_set
    
    def mutacao_filho(self, filho) -> list:
        for _ in range(int(self.num_cidades * self.taxa_mutacao)):
            a = np.random.randint(0, self.num_cidades)
            b = np.random.randint(0, self.num_cidades)

            filho[a], filho[b] = filho[b], filho[a]

        return filho
    
    def mutacao_populacao(self):
        populacao_mutada = []
        for filho in self.nova_populacao_set:
            populacao_mutada.append(self.mutacao_filho(filho))

        return populacao_mutada
    
    def algoritmo_genetico(self, num_interacao:int) -> None:
        melhor_solucao = [-1, np.inf, np.array([])]

        for i in range(num_interacao):

            if self.list_fitness.min() < melhor_solucao[1]:
                melhor_solucao[0] = i
                melhor_solucao[1] = self.list_fitness.min()
                melhor_solucao[2] = np.array(self.populacao_mutada)[self.list_fitness.min() == self.list_fitness]

            self.list_progenitores = self.selecao_progenitores()
            self.nova_populacao_set = self.gera_populacao()

            self.populacao_mutada = self.mutacao_populacao()

            self.melhor_solucao = melhor_solucao

if __name__ == '__main__':
    cidades = Cidades(list_nome, distancia_cidades, 100, 0.3)
    cidades.algoritmo_genetico(10000)
    print(cidades.melhor_solucao)
