import random
import numpy as np
from no import No


class BracoRobotico:

    def __init__(self):
        self.estado_inicial = [["_"], [10], [20]]
        # self.estado_objetivo = np.matrix([[20, "_", "_"], [10, "_", "_"], ["_", "_", "_"]])
        self.quantidade_casas = len(self.estado_inicial)
        self.posicao_braco = int(self.quantidade_casas / 2)
        self.dic_caixas_para_empilhar = dict()
        self.casas_reservadas_para_empilhar = []
        self.identifica_casas_reservadas_para_empilhar()

    def iniciar(self):
        # np.random.shuffle(self.estado_inicial)
        self.cria_dicionario_casas_para_empilhar()

        self.no_raiz = No(self.estado_inicial)
        return self.no_raiz

    def cria_dicionario_casas_para_empilhar(self):
        esteira = np.array(self.estado_inicial)

        for i, item in enumerate(esteira):
            if item != "_":
                self.dic_caixas_para_empilhar[i] = item

    def identifica_casas_reservadas_para_empilhar(self):
        for i in range(int(self.quantidade_casas / 3)):
            self.casas_reservadas_para_empilhar.append(i)

    def imprimir(self, no):
        estado = no.estado
        return "| " + estado[0] + " | " + estado[1] + " | " + estado[
            2] + " |\n| " + estado[3] + " | " + estado[4] + " | " + estado[
            5] + " |\n| " + estado[6] + " | " + estado[7] + " | " + estado[
            8] + " |"

    def testar_objetivo(self, no):
        return np.array_equal(no.estado, self.estado_objetivo)

    def gerar_sucessores(self, no):
        estado = no.estado
        nos_sucessores = []

        # posicao = np.where(estado == "_")[0][0] # posicao do maior valor buscando no dicionario

        expansoes = [self._direita, self._esquerda]  # nos vamos ter direita e esquerda e buscar qualquer caixa por enquanto
        random.shuffle(expansoes)

        for expansao in expansoes:
            no_sucessor = expansao(no)
            if no_sucessor is not None: nos_sucessores.append(no_sucessor)

        return nos_sucessores

    # movimento para esquerda
    def _esquerda(self, no):

        if self.posicao_braco not in [0]:
            # peça de baixo desce
            sucessor = np.copy(no.estado)
            self.posicao_braco = self.posicao_braco - 1

            while no.estado[self.posicao_braco][len(no.estado[self.posicao_braco]) - 1] != "_" and self.posicao_braco not in self.casas_reservadas_para_empilhar:
                print("A")

            return No(sucessor, no, "⬅️")
        else:
            None

    # movimento para direita
    def _direita(self, no):

        if self.posicao_braco not in [self.tamanho_linha_x_coluna[0] - 1]:
            # peça de baixo desce
            sucessor = np.copy(no.estado)
            return No(sucessor, no, "➡️")
        else:
            None

    # Heurística 1: Checar se os valores
    # esta heurística não é admissível, pois, pode dificultar
    # a chegada de um resultado final
    def heuristica2(self, no):
        estado = no.estado
        resultado = self.estado_objetivo
        return sum(1 for i in range(len(resultado)) if resultado[i] == estado[i])

    # Heurística 2: Distância para o resultado espero
    # Heurística adminissível, pois, sempre o resultado chega mais perto
    # Transformei o array em matriz para fazer cálculo de distância
    def heuristica(self, no):
        estado = no.estado
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
