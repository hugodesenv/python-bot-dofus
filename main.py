# Definindo bibliotecas
import pyautogui
import os, os.path
import time
from config.constantes import *
from lib.libCalculo import *
from lib.libMapa import *

# Variáveis públicas
PubCoordenadasMonitor = {}

itens_coleta = [
  ('urtiga', './img/planta/urtiga/'),
  ('salvia', './img/planta/salvia/'),
  ('freixo', './img/arvore/arvore_freixo/'),
  ('trevo', './img/planta/trevo/'),
  ('peixe', './img/peixe/')
]

# Função para verificar se existe a seta de troca de mapa
def existeSetaTrocaMapa(direcao):
  global PubCoordenadasMonitor
  pyautogui.moveTo(
      PubCoordenadasMonitor[direcao]['horizontal'], 
      PubCoordenadasMonitor[direcao]['vertical'], 
      0.2
  )
  return LibMapa.verificaImagemExiste('./img/seta/' + direcao)

# Função de coleta de itens
def coletarItem(nome, caminho_imagem):
  x, y, _, _ = LibMapa.verificaImagemExiste(caminho_imagem)
  if x > 0:
    print(f"--> Coletando {nome.capitalize()}")
    pyautogui.click(x + 5, y + 5)
    time.sleep(8)
    return True
  return False

# Função principal
def main():
  i = 0
  atualX = int(input('X: '))
  atualY = int(input('Y: '))
    
  global PubCoordenadasMonitor
  PubCoordenadasMonitor = LibMapa.mapearCantosDirecionaisDaTela()
    
  while True:
    # Coleta de recursos
    for nome, caminho in itens_coleta:
      if coletarItem(nome, caminho):
        break  # Sai da coleta para realizar a próxima movimentação

    # Saída de batalha
    if LibMapa.sairDaBatalha():
      existeSetaTrocaMapa('esquerda')
      atualX = POSICAO_RESPAWM[0]
      atualY = POSICAO_RESPAWM[1]
      LibMapa.movimentarPersonagem(atualX, atualY)
      continue

    # Verifica se chegou ao destino
    destX, destY = coordenadas[i]
    if (atualX, atualY) == (destX, destY):
      i = (i + 1) % len(coordenadas)  # Move para o próximo ponto ou reinicia a lista
      continue

    # Busca nova direção
    for X_Y in ['x', 'y']:
      if X_Y == 'x':
        proximaDirecao = LibMapa.buscarNovaDirecao('x', atualX, destX)
      else:
        proximaDirecao = LibMapa.buscarNovaDirecao('y', atualY, destY)
            
      # Movimenta o personagem se a direção for válida
      if proximaDirecao and existeSetaTrocaMapa(proximaDirecao):
        atualX, atualY = LibCalculo.calcularProximaCoordenada(proximaDirecao, atualX, atualY)
        LibMapa.movimentarPersonagem(atualX, atualY)
        break
      else:
        print(f"Direção '{proximaDirecao}' bloqueada ou inválida. Tentando outra direção.")
        
main()