import random
import numpy as np
from no import No


class BracoRobotico:

    def __init__(self):
        self.estado_objetivo = np.array([
            3, 0, 0,
            30, 20, 10,
            0, 0, 0,
            0, 0, 0,
            0, 0, 0
        ])
        self.estado_inicial = np.array([
            3, 0, 0,
            0, 0, 0,
            20, 0, 0,
            10, 0, 0,
            30, 0, 0
        ])

    def iniciar(self):
        self.no_raiz = No(self.estado_inicial)
        self.procurar_caixa(self.no_raiz)
        return self.no_raiz

    def imprimir(self, no):
        estado = self.estado_inicial
        labirinto = ""

        # for i in range(3):
        #   for j in range(5):
        #     labirinto += estado[5*i + j]
        #   labirinto += "\n"
        # return labirinto
        e = "   "
        return f"""
       \r{estado[5]}{e}{estado[8]}{e}{estado[11]}{e}{estado[14]}
       \r{estado[4]}{e}{estado[7]}{e}{estado[10]}{e}{estado[13]}
       \r{estado[3]}{e}{estado[6]}{e}{estado[9]}{e}{estado[12]}
       """

    def testar_objetivo(self, no):
        return np.array_equal(no.estado, self.estado_objetivo)

    # Função que gera os sucessores válidos
    # a partir de um estado válido
    def gerar_sucessores(self, no):
        estado = no.estado
        nos_sucessores = []

        # encontra a posição do _
        # posicao = np.where(estado == "_")[0][0]  # posicao do maior valor buscando no dicionario
        posicao = estado[0] # posicao do braco do robo

        expansoes = [self._direita,
                     self._esquerda]  # nos vamos ter direita e esquerda e buscar qualquer caixa por enquanto
        random.shuffle(expansoes)
        for expansao in expansoes:
            no_sucessor = expansao(posicao, no)
            if no_sucessor is not None: nos_sucessores.append(no_sucessor)

        return nos_sucessores

    def procurar_caixa(self, no):
        self.caixas = []
        for i in range(3, len(self.estado_inicial), 3):
            caixa_peso = self.estado_inicial[i]
            if caixa_peso != 0:
                self.caixas.append((i, caixa_peso))

    def pegar_caixa(self, no):
        print()

    def colocar_caixa(self, no):
        print()
    
    def _esquerda(self, posicao, no):
        # movimento para esquerda
        if posicao not in [0, 1, 2, 3]:
            # peça de baixo desce
            sucessor = np.copy(no.estado)
            sucessor[posicao] = sucessor[posicao - 1]
            sucessor[posicao - 1] = "_"
            return No(sucessor, no, "⬅️")
        else:
            None

    def _direita(self, posicao, no):
        # movimento para direita
        ## Não gera se estiver na direita
        if posicao not in [12]:
            # peça de baixo desce
            sucessor = np.copy(no.estado)
            sucessor[posicao] = sucessor[posicao + 1]
            sucessor[posicao + 1] = "_"
            return No(sucessor, no, "➡️")
        else:
            None

    # Heurística 1: Checar se os valores
    # esta heurística não é admissível, pois, pode dificultar
    # a chegada de um resultado final
    # def heuristica2(self, no):
    #   estado = no.estado
    #   resultado = self.estado_objetivo
    #   return sum(1 for i in range(len(resultado)) if resultado[i] == estado[i])
    #
    # # Heurística 2: Distância para o resultado espero
    # # Heurística adminissível, pois, sempre o resultado chega mais perto
    # # Transformei o array em matriz para fazer cálculo de distância
    # def heuristica(self, no):
    #   estado = no.estado
    #   resultado = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "_"]]
    #   estado_matriz = [estado[0:3], estado[3:6], estado[6:9]]
    #
    #   soma = 0
    #
    #   for i in range(len(resultado)):
    #     for j in range(len(resultado[i])):
    #       valor = resultado[i][j]
    #       soma = soma + self._distancia_manhattan(valor, estado_matriz, i, j)
    #
    #   return soma
    #
    # # Distância de Manhattan: d = |xi-xj| + |yi-yj|
    # def _distancia_manhattan(self, valor, estado, i, j):
    #   for k in range(len(estado)):
    #     for h in range(len(estado[k])):
    #       if valor == estado[k][h]: return abs(i - k) + abs(j - h)
    #
    # # Função de custo: Quando custa mover de um
    # # estado_origem para estado_destino. No Quebra Cabeça
    # # de 8, este custo é fixo e arbitrariamente será 1.
    # def custo(self, no, no_destino):
    #   return 1
