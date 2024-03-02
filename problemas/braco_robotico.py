import random
import numpy as np
from no import No

class BracoRobotico:

  def __init__(self):
    self.estado_inicial = np.matrix([["_", 10, 20], ["_", "_", "_"], ["_", "_", "_"], ["_", "R", "_"]])
    self.estado_objetivo = np.matrix([[20, "_", "_"], [10, "_", "_"], ["_", "_", "_"], ["_", "R", "_"]])

  def iniciar(self):
    # np.random.shuffle(self.estado_inicial)

    self.no_raiz = No(self.estado_inicial)
    return self.no_raiz

  def imprimir(self, no):
    estado = no.estado
    return "| " + estado[0] + " | " + estado[1] + " | " + estado[
        2] + " |\n| " + estado[3] + " | " + estado[4] + " | " + estado[
            5] + " |\n| " + estado[6] + " | " + estado[7] + " | " + estado[
                8] + " |"

  def testar_objetivo(self, no):
    return np.array_equal(no.estado, self.estado_objetivo)

  # Função que gera os sucessores válidos
  # a partir de um estado válido
  def gerar_sucessores(self, no):
    estado = no.estado
    nos_sucessores = []

    # encontra a posição do _
    posicao = np.where(estado == "_")[0][0] # posicao do maior valor buscando no dicionario

    expansoes = [self._direita, self._esquerda] # nos vamos ter direita e esquerda e buscar qualquer caixa por enquanto
    random.shuffle(expansoes)
    for expansao in expansoes:
      no_sucessor = expansao(posicao, no)
      if no_sucessor is not None: nos_sucessores.append(no_sucessor)

    return nos_sucessores

  def _esquerda(self, posicao, no):
    # movimento para esquerda
    if posicao not in [0, 3, 6]:
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
    if posicao not in [2, 5, 8]:
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
