# definindo bibliotecas
import pyautogui
import os, os.path
import time
from config.constantes import *
from lib.libCalculo import *
from lib.libMapa import *

# variaveis pubs
PubCoordenadasMonitor = {}

# funcao: verifica se existe a seta de direcionamento no mapa
def existeSetaTrocaMapa(dir):
  #print("** Dentro da funcao existeSetaTrocaMapa")
  global PubCoordenadasMonitor
  
  pyautogui.moveTo(
    PubCoordenadasMonitor[dir]['horizontal'], 
    PubCoordenadasMonitor[dir]['vertical'], 
    0.2
  )
    
  return LibMapa.verificaImagemExiste('./img/seta/' + dir)

# funcao: principal
def main():
  #--> entrando com a posiçao inicial do nosso personagem
  i_pos_personagem_x = int(input('X: '))
  i_pos_personagem_y = int(input('Y: '))
  
  indice = 0
  
  #--> mapeando os cantos direcionais da tela
  global PubCoordenadasMonitor
  PubCoordenadasMonitor = LibMapa.mapearCantosDirecionaisDaTela()

  while True:  
    #--> variavel para controle quando precisamos analisar a saida mais proxima 
    proximaDirecao = ''
  
    for X_Y in ['x', 'y']:      
      if indice == len(obj_coordenadas_recursos): indice = 0
      
      i_pos_destino_x = obj_coordenadas_recursos[indice][0]
      i_pos_destino_y = obj_coordenadas_recursos[indice][1]
      
      ###########################TESTE MELHORARRR#######################################
      print("--> Teste Hugo, coletando Urtiga")
      x, y, _, _ = LibMapa.verificaImagemExiste('./img/planta/urtiga/')
      if x > 0:
        pyautogui.click(x + 5, y + 5)
        time.sleep(8)
        
      print("--> Teste Hugo, coletando Salvia")
      x, y, _, _ = LibMapa.verificaImagemExiste('./img/planta/salvia/')
      if x > 0:
        pyautogui.click(x + 5, y + 5)
        time.sleep(8) 
        
      print("--> Teste Hugo, coletando Freixo")
      x, y, _, _ = LibMapa.verificaImagemExiste('./img/arvore/arvore_freixo/')
      if x > 0:
        pyautogui.click(x + 5, y + 5)
        time.sleep(8) 
        
      print("--> Teste Hugo, coletando Trevo")
      x, y, _, _ = LibMapa.verificaImagemExiste('./img/planta/trevo/')
      if x > 0:
        pyautogui.click(x + 5, y + 5)
        time.sleep(8) 
      ##################################################################
        

      #--> esquema para sair da batalha
      if LibMapa.sairDaBatalha():
        #print('\nVerificando se o personagem está em batalha')
        if True:
          #print('O personagem esta em batalha')
          existeSetaTrocaMapa('esquerda')
          i_pos_personagem_x = POSICAO_RESPAWM[0]
          i_pos_personagem_y = POSICAO_RESPAWM[1]
            
          pyautogui.click()
          time.sleep(TEMPO_TROCA_MAPA) 
          continue
        else: 
          print('\n##HUGO::: Tratar aqui quando virar fantasma...')
          
      #--> esquema para buscar uma nova rota com base no indice 
      if (i_pos_personagem_x, i_pos_personagem_y) == (i_pos_destino_x, i_pos_destino_y):
        indice += 1
        continue
    
      proximaDirecao = ''
           
      if X_Y == 'x':
        proximaDirecao = LibMapa.buscarNovaDirecao('x', i_pos_personagem_x, i_pos_destino_x)
      else:
        proximaDirecao = LibMapa.buscarNovaDirecao('y', i_pos_personagem_y, i_pos_destino_y)
      
      if proximaDirecao == '':
        continue
      
      #--> se existe a seta para trocar de mapa, entao vamos la:
      if existeSetaTrocaMapa(proximaDirecao):
        i_pos_personagem_x, i_pos_personagem_y = LibCalculo.calcularProximaCoordenada(proximaDirecao, i_pos_personagem_x, i_pos_personagem_y)     
        
        print(f"Próxima posição X: {i_pos_personagem_x}")
        print(f"Próxima posição Y: {i_pos_personagem_y}")
        
        pyautogui.click()
        time.sleep(TEMPO_TROCA_MAPA) 
        
      # se nao existir, vamos andar em ambas direcoes diferentes ate encontrar a saida
      # quando encontrar, eu reseto
      else:   
        for d in PubCoordenadasMonitor[proximaDirecao]['direcoes_inversas']:
          while True:
            if existeSetaTrocaMapa(d):
              i_pos_personagem_x, i_pos_personagem_y = LibCalculo.calcularProximaCoordenada(d, i_pos_personagem_x, i_pos_personagem_y) 
              pyautogui.click()
              time.sleep(TEMPO_TROCA_MAPA)
            
            # quando chegar ao fim da direcao (se existir mapa que isso pode ocorrer), tentamos o processo contrário
            # eu nao sei se é possivel ir tanto pra direita e pra esquerda por exemplo e nao existir a saida pra cima
            # nesse caso, eu trato num futuro se houver.
            else: 
              break        
            
            if existeSetaTrocaMapa(proximaDirecao):
              i_pos_personagem_x, i_pos_personagem_y = LibCalculo.calcularProximaCoordenada(proximaDirecao, i_pos_personagem_x, i_pos_personagem_y) 
              indice = 0
              pyautogui.click()
              time.sleep(TEMPO_TROCA_MAPA)
              
main()