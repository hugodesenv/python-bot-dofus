# definindo bibliotecas
import pyautogui
import os, os.path
import time
from config.constantes import *
from lib.libCalculo import *
from lib.libMapa import *

# objeto que armazena em qual X e Y o ponteiro do mouse ficarÃ¡ para trocar de mapa:
obj_coordenadas_monitor = {
  'cima': {
    'horizontal': 1200,
    'vertical': 0,
    'direcoes_inversas': ['esquerda', 'direita']
  },
  'baixo': {
    'horizontal': 1200,
    'vertical': 0,
    'direcoes_inversas': ['esquerda', 'direita']
  },
  'esquerda': {
    'horizontal': 0,
    'vertical': 200,
    'direcoes_inversas': ['cima', 'baixo']
  },
  'direita': {
    'horizontal': 0,
    'vertical': 200,
    'direcoes_inversas': ['cima', 'baixo']
  },
}

'''
  exemplo do objeto abaixo:
  obj_mapa_mapeado = [
    [9, -25]{
      lados_bloqueados: ['direita', 'baixo'],
      #saidas: [{'x': 10, 'y': 20}, {'x': 2, 'y': -3}]
    }
  ]
'''

# objeto que guardamos o mapeamento do nosso mapa atual (lados que nao podem ser clicaveis etc)
obj_mapa_mapeado = {}

# funcao: verifica se existe a seta de direcionamento no mapa
def existe_seta_troca_mapa(pdirecao):
  x = obj_coordenadas_monitor[pdirecao]['horizontal']
  y = obj_coordenadas_monitor[pdirecao]['vertical'] 
  
  pyautogui.moveTo(x, y, 0.2)  
  
  return LibMapa.obterPontoDaImagem(pCaminhoImagem='./img/seta/' + pdirecao)

# funcao: verifica e sai da batalha se o personagem estiver
def verifica_personagem_em_batalha():
  b_embatalha = False

  for i in ordens_cliques_sair_da_batalha:
    x, y, _, _ = LibMapa.verificaImagemExiste(i)
    if x > 0:
      b_embatalha = True
      pyautogui.moveTo(x, y)  
      pyautogui.click()
      time.sleep(2)
    else:
      break
      
  return b_embatalha

# funcao: calcular a rota mais proxima entre dois ponto
#def calcular_peso_distancia_manhattan(ix_A, iy_A, ix_B, iy_B):
#  return abs(ix_A - ix_B) + abs(iy_A - iy_B)

# funcao: principal
def main():
  i_pos_personagem_x = int(input('X: '))
  i_pos_personagem_y = int(input('Y: '))
  indice_coord_destino = 0
  
  time.sleep(4)
  
  # obtendo o tamanho da tela para mapearmos as setas direcionais
  screen_width, screen_height = pyautogui.size()
  
  #  mapeando seta direcional da direita
  print('\nMapeando seta direcional direita...')
  indice_pixel = screen_width + 15
  
  while True:
    indice_pixel -= 15
    pyautogui.moveTo(indice_pixel, obj_coordenadas_monitor['direita']['vertical'])

    _, _, x, y = LibMapa.verificaImagemExiste('./img/seta/direita')
    
    if x > 0:
      obj_coordenadas_monitor['direita']['horizontal'] = x
      break
    
  # mapeando seta direcional de cima
  print('\nMapeando seta direcional de cima')
  indice_pixel = 0
  
  while True:
    indice_pixel += 15
    pyautogui.moveTo(obj_coordenadas_monitor['cima']['horizontal'], indice_pixel)
    
    _, _, x, y = LibMapa.verificaImagemExiste('./img/seta/cima')
  
    if x > 0:
      obj_coordenadas_monitor['cima']['vertical'] = y
      break
  
  # mapeando seta direcional de baixo
  print('\nMapeando seta direcional de baixo')
  indice_pixel = screen_height + 15
  
  while True:
    indice_pixel -= 15
    pyautogui.moveTo(obj_coordenadas_monitor['baixo']['horizontal'], indice_pixel)
    
    _, _, x, y = LibMapa.verificaImagemExiste('./img/seta/baixo')
    
    if x > 0:
      obj_coordenadas_monitor['baixo']['vertical'] = y
      break
  
  # mapeando seta direcional da esquerda
  print('\nMapeando seta direcional da esquerda')
  indice_pixel = 0
  
  while True:
    indice_pixel += 15
    pyautogui.moveTo(indice_pixel, obj_coordenadas_monitor['esquerda']['vertical'])
        
    _, _, x, y = LibMapa.verificaImagemExiste('./img/seta/esquerda')    
    
    if x > 0:
      obj_coordenadas_monitor['esquerda']['horizontal'] = x
      break
  
  #---------------------------------------------------------------------------------------------------------------------
  # funcao anonima 
  def _key_pos_atual(): 
    return (i_pos_personagem_x, i_pos_personagem_y)
  #---------------------------------------------------------------------------------------------------------------------                                                                                      
  
  while True:  
    # variavel para controle quando precisamos analisar a saida mais proxima 
    direcoes_inversas = []
    s_direcao_sugestiva = ''
  
    for X_Y in ['x', 'y']:      
      if indice_coord_destino == len(obj_coordenadas_recursos):
        indice_coord_destino = 0
      
      i_pos_destino_x = obj_coordenadas_recursos[indice_coord_destino][0]
      i_pos_destino_y = obj_coordenadas_recursos[indice_coord_destino][1]

      # faz o mapeamento das posicoes possiveis do mapa atual
      print('Realizando o mapeamento das coordenadas do mapa atual')
      
      if _key_pos_atual() not in obj_mapa_mapeado: 
        obj_mapa_mapeado[_key_pos_atual()] = { 'lados_bloqueados': [], 'saidas': [] }  
        for s_direcao in obj_coordenadas_monitor.keys():
          if not existe_seta_troca_mapa(s_direcao):
            obj_mapa_mapeado[_key_pos_atual()]['lados_bloqueados'].append(s_direcao)

      # coleta o recurso do mapa
      print('Coletando recursos')
      
      for caminho in obj_listagem_recursos:  
        s_caminho_recurso = './img' + caminho + '/'
        x, y, _, _ = LibMapa.verificaImagemExiste(s_caminho_recurso)
        
        if x > 0: 
          pyautogui.moveTo(x + 5, y + 5)
          pyautogui.click()
          time.sleep(10)
  
      # esquema para sair da batalha
      print('Verificando se o personagem está em batalha')
      
      if verifica_personagem_em_batalha():
        if True:
          print('O personagem esta em batalha')
          existe_seta_troca_mapa('esquerda')
          i_pos_personagem_x = POSICAO_RESPAWM[0]
          i_pos_personagem_y = POSICAO_RESPAWM[1]
            
          pyautogui.click()
          time.sleep(TEMPO_TROCA_MAPA) 
          continue
        else: 
          print('\n##HUGO::: Tratar aqui quando virar fantasma...')
          
      # esquema par abuscar uma nova rota com base no indice 
      if _key_pos_atual() == (i_pos_destino_x, i_pos_destino_y):
        print('Chegando a posicao destino, vamos resetar')
        indice_coord_destino += 1
        continue
    
      s_direcao_sugestiva = ''
            
      if X_Y == 'x':
        s_direcao_sugestiva = LibMapa.buscarNovaDirecao('x', i_pos_personagem_x, i_pos_destino_x)
      else:
        s_direcao_sugestiva = LibMapa.buscarNovaDirecao('y', i_pos_personagem_y, i_pos_destino_y)
      
      if s_direcao_sugestiva == '':
        continue
      
      # se existe a seta para trocar de mapa, entao vamos la:
      if existe_seta_troca_mapa(s_direcao_sugestiva):
        i_pos_personagem_x, i_pos_personagem_y = LibCalculo.calcularProximaCoordenada(s_direcao_sugestiva, i_pos_personagem_x, i_pos_personagem_y)     
        
        pyautogui.click()
        time.sleep(TEMPO_TROCA_MAPA) 
        
      # se nao existir, vamos andar em ambas direcoes diferentes ate encontrar a saida
      # quando encontrar, eu reseto
      else: 
        print('Buscando uma direcao alternativa')
            
        direcoes_inversas = obj_coordenadas_monitor[s_direcao_sugestiva]['direcoes_inversas']
       
        for direcao in direcoes_inversas:
          while True:
            if existe_seta_troca_mapa(direcao):
              i_pos_personagem_x, i_pos_personagem_y = LibCalculo.calcularProximaCoordenada(direcao, i_pos_personagem_x, i_pos_personagem_y) 
              
              pyautogui.click()
              time.sleep(TEMPO_TROCA_MAPA)
            
            # quando chegar ao fim da direcao (se existir mapa que isso pode ocorrer), tentamos o processo contrário
            # eu nao sei se é possivel ir tanto pra direita e pra esquerda por exemplo e nao existir a saida pra cima
            # nesse caso, eu trato num futuro se houver.
            else: 
              break        
            
            if existe_seta_troca_mapa(s_direcao_sugestiva):
              i_pos_personagem_x, i_pos_personagem_y = LibCalculo.calcularProximaCoordenada(s_direcao_sugestiva, i_pos_personagem_x, i_pos_personagem_y) 
              
              indice_coord_destino = 0
              pyautogui.click()
              time.sleep(TEMPO_TROCA_MAPA)
              
main()