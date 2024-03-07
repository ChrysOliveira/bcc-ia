import random
import numpy as np
from no import No


class BracoRobotico:

    def __init__(self):
      self.caixas = None
      self.no_raiz = None
      self.estado_inicial = np.array([
        3, 0, 0,
        0, 0, 0,
        20, 0, 0,
        10, 0, 0,
        30, 0, 0
      ])
      self.estado_objetivo = np.array([
        1, 0, 0,
        30, 20, 10,
        0, 0, 0,
        0, 0, 0,
        0, 0, 0
      ])

    def iniciar(self):
        self.no_raiz = No(self.estado_inicial)
        self.procurar_caixa(self.no_raiz.estado)
        return self.no_raiz

    def procurar_caixa(self, estado_atual):
        self.caixas = []
        for i in range(6, len(estado_atual), 3):
            caixa_peso = estado_atual[i]
            if caixa_peso != 0:
                self.caixas.append((i, caixa_peso))

    def imprimir(self, no):
      estado = no.estado

      e = "   "
      print(f"""
     \r{estado[5]}{e}{estado[8]}{e}{estado[11]}{e}{estado[14]}
     \r{estado[4]}{e}{estado[7]}{e}{estado[10]}{e}{estado[13]}
     \r{estado[3]}{e}{estado[6]}{e}{estado[9]}{e}{estado[12]}
     """)

    def testar_objetivo(self, no):
        return np.array_equal(no.estado, self.estado_objetivo)

    def gerar_sucessores(self, no):
        estado = no.estado
        nos_sucessores = []

        posicao = estado[0] # posicao do braco do robo

        valores_direta = [tupla[0] for tupla in self.caixas if tupla[0] > posicao]
        random.shuffle(valores_direta)

        if valores_direta is not None:
            for i in valores_direta:

                posicao_nova_caixa = i

                expansoes = [self._direita]
                # random.shuffle(expansoes)

                for expansao in expansoes:
                    no_sucessor = expansao(posicao, no, posicao_nova_caixa)
                    if no_sucessor is not None: nos_sucessores.append(no_sucessor)




        return nos_sucessores

    def _direita(self, posicao, no, posicao_nova_caixa):
        if posicao not in [4]:
            sucessor = np.copy(no.estado)

            self.pegar_caixa(sucessor, posicao_nova_caixa)

            self.colocar_caixa(sucessor)

            self.procurar_caixa(sucessor)
            return No(sucessor, no, "➡️")
        else:
            None

    # def _esquerda(self, posicao, no):
    #     valores_esquerda = [tupla[0] for tupla in self.caixas if tupla[0] < posicao]
    #     if posicao not in [1] and valores_esquerda:
    #         sucessor = np.copy(no.estado)
    #
    #         random.shuffle(valores_esquerda)
    #         posicao_nova_caixa = valores_esquerda[0]
    #         self.pegar_caixa(sucessor, posicao_nova_caixa)
    #
    #         self.colocar_caixa(sucessor)
    #
    #         self.procurar_caixa(sucessor)
    #         return No(sucessor, no, "⬅️")
    #     else:
    #         None

    def calcula_posicao_braco(self, casa_atual):
      return casa_atual // 3

    def pegar_caixa(self, no_sucessor, nova_posicao):
        no_sucessor[0] = nova_posicao // 3
        no_sucessor[1], no_sucessor[nova_posicao] = no_sucessor[nova_posicao], no_sucessor[1]

    def colocar_caixa(self, no_sucessor):
        posicao_livre = None

        for i in range(3,6):
            if no_sucessor[i] == 0:
                posicao_livre = i
                break

        no_sucessor[0] = posicao_livre // 3

        no_sucessor[posicao_livre], no_sucessor[1] = no_sucessor[1], no_sucessor[posicao_livre]


        #NAO ESQUECER DE ATUALIZAR O no_sucessor[1] para 0



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
