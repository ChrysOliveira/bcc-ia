import random
import numpy as np
import copy
from estruturas.pilha import Pilha
from no import No


class BracoRobotico:

    def __init__(self):
        self.posicoes_iniciais = [None, 10, 20]
        self.estado_inicial = np.array([Pilha(), Pilha(), Pilha()], dtype=Pilha)
        # self.estado_objetivo = np.matrix([[20, "_", "_"], [10, "_", "_"], ["_", "_", "_"]])
        self.quantidade_casas = len(self.estado_inicial)
        self.posicao_braco = int(self.quantidade_casas / 2)
        self.dic_caixas_para_empilhar = dict()
        self.casas_reservadas_para_empilhar = []
        self.esteira_ja_foi_organizada = False

    def iniciar(self):
        # np.random.shuffle(self.posicoes_iniciais)
        self.popula_posicoes_iniciais()
        self.cria_dicionario_casas_para_empilhar()
        self.identifica_casas_reservadas_para_empilhar()

        self.no_raiz = No(self.estado_inicial)
        return self.no_raiz

    def popula_posicoes_iniciais(self):
        for i, item in enumerate(self.posicoes_iniciais):
            self.estado_inicial[i].push(item)
            self.estado_inicial[i].push(None)
            self.estado_inicial[i].push(None)

    def cria_dicionario_casas_para_empilhar(self):
        esteira = self.estado_inicial

        for i, item in enumerate(esteira):
            if item.ultimo_valor() != "_":
                self.dic_caixas_para_empilhar[i] = item.ultimo_valor()

    def identifica_casas_reservadas_para_empilhar(self):
        for i in range(int(self.quantidade_casas / 3)):
            self.casas_reservadas_para_empilhar.append(i)

    def imprimir(self, no):
        estado = copy.deepcopy(no.estado)

        for i, item in enumerate(estado):
            while(item.tamanho() > 0):
                print(item.pop(), end=" ")
            print()

    def testar_objetivo(self, no):
        caixas_somente_nas_pilhas_e_ordenado = True
        estado = copy.deepcopy(no.estado)
        for i in self.casas_reservadas_para_empilhar:
            if(estado[i].esta_sem_caixa()):
                caixas_somente_nas_pilhas_e_ordenado = False
            else:
                menor_valor = estado[i].pop()
                meio_valor = estado[i].pop()
                maior_valor = estado[i].pop()
                if(menor_valor > meio_valor or meio_valor > maior_valor):
                    caixas_somente_nas_pilhas_e_ordenado = False

        for i in range(len(self.casas_reservadas_para_empilhar), self.quantidade_casas):
            if not estado[i].esta_sem_caixa():
                caixas_somente_nas_pilhas_e_ordenado = False

        return caixas_somente_nas_pilhas_e_ordenado

    def gerar_sucessores(self, no):
        estado = copy.deepcopy(no.estado)

        nos_sucessores = []

        if not self.esteira_ja_foi_organizada:

            no_sucessor = self.libera_pilhas_reservadas_esquerda(no)
            if no_sucessor is not None:
                nos_sucessores.append(no_sucessor)
                return nos_sucessores

        self.imprimir(no) #CHRYS: estou vendo se fez o swap e atualizou a posicao do braco
        if self.esteira_ja_foi_organizada:

            expansoes = [self._esquerda, self._direita]  # nos vamos ter direita e esquerda e buscar qualquer caixa por enquanto
            # random.shuffle(expansoes)

            for expansao in expansoes:
                no_sucessor = expansao(no)
                if no_sucessor is not None: nos_sucessores.append(no_sucessor)

        return nos_sucessores

    def libera_pilhas_reservadas_esquerda(self, no):
        sucessor = copy.deepcopy(no.estado)
        custo_movimentacao = 0.0

        for i in self.casas_reservadas_para_empilhar:
            if not no.estado[i].esta_sem_caixa():
                caixa = no.estado[i]
                nova_posicao = i + 1

                while no.estado[nova_posicao] is not None or nova_posicao in self.casas_reservadas_para_empilhar:
                    nova_posicao = nova_posicao + 1

                no.estado[i] = None
                no.estado[nova_posicao] = caixa

                # if i == len(self.casas_reservadas_para_empilhar) - 1:
                #     self.esteira_ja_foi_organizada = True
                self.posicao_braco = nova_posicao
                return No(sucessor, no, "🔧")

            if i == len(self.casas_reservadas_para_empilhar) - 1:
                self.esteira_ja_foi_organizada = True

    # movimento para esquerda
    def _esquerda(self, no):

        if self.posicao_braco not in [0]:
            # peça de baixo desce
            sucessor = copy.deepcopy(no.estado)
            custo_movimentacao = 0.0
            self.posicao_braco = self.posicao_braco - 1

            # while no.estado[self.posicao_braco][len(no.estado[self.posicao_braco]) - 1] != "_" and self.posicao_braco not in self.casas_reservadas_para_empilhar:
            #     print("A")

            return No(sucessor, no, "⬅️")
        else:
            None

    # movimento para direita
    def _direita(self, no):

        if self.posicao_braco not in [self.quantidade_casas - 1]:
            # peça de baixo desce
            sucessor = copy.deepcopy(no.estado)
            custo_movimentacao = 0.0
            return No(sucessor, no, "➡️")
        else:
            None

    # Heurística 1: Checar se os valores
    # esta heurística não é admissível, pois, pode dificultar
    # a chegada de um resultado final
    def heuristica2(self, no):
        estado = copy.deepcopy(no.estado)
        resultado = self.estado_objetivo
        return sum(1 for i in range(len(resultado)) if resultado[i] == estado[i])

    # Heurística 2: Distância para o resultado espero
    # Heurística adminissível, pois, sempre o resultado chega mais perto
    # Transformei o array em matriz para fazer cálculo de distância
    def heuristica(self, no):
        estado = copy.deepcopy(no.estado)
        resultado = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]
        estado_matriz = [estado[0:3], estado[3:6], estado[6:9]]

        soma = 0

        for i in range(len(resultado)):
            for j in range(len(resultado[i])):
                valor = resultado[i][j]
                soma = soma + self._distancia_manhattan(valor, estado_matriz, i, j)

        return soma

    # Distância de Manhattan: d = |xi-xj| + |yi-yj|
    def _distancia_manhattan(self, valor, estado, i, j):
        for k in range(len(estado)):
            for h in range(len(estado[k])):
                if valor == estado[k][h]: return abs(i - k) + abs(j - h)

    # Função de custo: Quando custa mover de um
    # estado_origem para estado_destino. No Quebra Cabeça
    # de 8, este custo é fixo e arbitrariamente será 1.
    def custo(self, no, no_destino):
        return 1
