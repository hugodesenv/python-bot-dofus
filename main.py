# definindo bibliotecas
import pyautogui
import os, os.path
import time

TEMPO_TROCA_MAPA = 8
QTD_PIXEL_SETA_DIRECIONAL = 10          

# objeto que armazena o caminho dos itens
obj_listagem_recursos = [
  '/agua',
  '/arvore/arvore_freixo',
  '/arvore/arvore_boldo',
  '/arvore/arvore_castanheiro',
  '/planta/urtiga'
]

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

# coordenadas dos recursos a serem coletados (hoje estou trabalhando apenas com urtiga e agua, depois verificar se precisar de mais coisa)
obj_coordenadas_recursos =  [
  [1,-27], 
  [1, -22], 
  [2, -21], 
  [2, -30], 
  [3, -30], 
  [3, -31], 
  [3, -20], 
  [4, -20], 
  [4, -31], 
  [5, -30], 
  [5, -29], 
  [6, -30], 
  [6, -26], 
  [7, -26], 
  [7, -22], 
  [8, -22], 
  [7, -21], 
  [7, -16], 
  [1, -16], 
  [1, -15], 
  [4, -15], 
  [3, -16], 
  [3, -14], 
  [9, -14], 
  [10, -13], 
  [3, -13], 
  [3, -12], 
  [11, -12], 
  [9, -11], 
  [3, -11]
]

POSICAO_RESPAWM = [6, -19]

# com base no caminho fornecido, verificamos se a imagem existe no mapa atual
# eu coloquei um delay de 5 segundos quando nao encontrar a imagem pra forcar ele encontrar
def checar_imagem_no_mapa(s_caminho_imagem, f_confidence, i_qtde_repeticao, i_delay):
  posicao = None
  for i in range(i_qtde_repeticao):
    for imagem in os.listdir(s_caminho_imagem):
      try:
        posicao = pyautogui.locateOnScreen(s_caminho_imagem + imagem, confidence=f_confidence)  
      except: pass
      
    if posicao: 
      break
    
    time.sleep(i_delay)
    
  return posicao

# funcao: verifica se existe a seta de direcionamento no mapa
def existe_seta_troca_mapa(pdirecao):
  x = obj_coordenadas_monitor[pdirecao]['horizontal']
  y = obj_coordenadas_monitor[pdirecao]['vertical'] 
  
  pyautogui.moveTo(x, y, 0.2)  
  
  return checar_imagem_no_mapa('./img/seta/' + pdirecao + '/', 0.4, 1, 1)

# funcao interna para definirmos a movimentacao do personagem
def calcular_troca_mapa(pdirecao, i_pos_personagem_x, i_pos_personagem_y):
  if pdirecao == 'direita':
    i_pos_personagem_x += 1
  elif pdirecao == 'esquerda':
    i_pos_personagem_x -= 1
  elif pdirecao == 'baixo':
    i_pos_personagem_y += 1
  elif pdirecao == 'cima':
    i_pos_personagem_y -= 1
  return i_pos_personagem_x, i_pos_personagem_y

# funcao: com base na direcao, calculamos a nova rota
def buscar_nova_direcao(x_ou_y_str, posicao_atual, posicao_destino):
  orientacao = {'x': ['direita', 'esquerda'], 'y': ['baixo', 'cima']}
  
  if posicao_destino > posicao_atual:
    return orientacao[x_ou_y_str][0]
  elif posicao_destino < posicao_atual:
    return orientacao[x_ou_y_str][1]
  else:
    return ''

# funcao: verifica e sai da batalha se o personagem estiver
def verifica_personagem_em_batalha():
  b_embatalha = False
  ordens_cliques = [
    './img/util/batalha/sair/',
    './img/util/batalha/confirmar/',
    './img/util/batalha/fechar/'
  ]
  
  for i in ordens_cliques:
    posicao = checar_imagem_no_mapa(i, 0.8, 2, 2)
    if posicao:
      b_embatalha = True
      pyautogui.moveTo(posicao[0], posicao[1])  
      pyautogui.click()
      time.sleep(2)
      
  return b_embatalha

# funcao: calcular a rota mais proxima entre dois ponto
#def calcular_peso_distancia_manhattan(ix_A, iy_A, ix_B, iy_B):
#  return abs(ix_A - ix_B) + abs(iy_A - iy_B)

# funcao: setas
def preparar_coordenadas_setas_direcionais():
  for d in obj_coordenadas_monitor:
    posicao_seta = None
    pixel = 0

    while posicao_seta == None:
      pixel += QTD_PIXEL_SETA_DIRECIONAL
      
      if obj_coordenadas_monitor[d]['horizontal'] == 0:
        pyautogui.moveTo(pixel, obj_coordenadas_monitor[d]['vertical'])
      else:
        pyautogui.moveTo(obj_coordenadas_monitor[d]['horizontal'], pixel)
        
      posicao_seta = checar_imagem_no_mapa('./img/seta/' + d + '/', 0.8, 1, 0)
      
      if posicao_seta:
        obj_coordenadas_monitor[d]['horizontal'] = posicao_seta.left
        obj_coordenadas_monitor[d]['vertical'] = posicao_seta.top
        time.sleep(2)

# funcao: principal
def main():
  i_pos_personagem_x = int(input('X: '))
  i_pos_personagem_y = int(input('Y: '))
  indice_coord_destino = 0
  
  time.sleep(4)
  
  # fazemos a analise de coordenadas do monitor, guardando o posicionamento das setas
  preparar_coordenadas_setas_direcionais()
  
  #---------------------------------------------------------------------------------------------------------------------
  # funcao anonima 
  def _key_pos_atual(): return (i_pos_personagem_x, i_pos_personagem_y)
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
      if _key_pos_atual() not in obj_mapa_mapeado: 
        obj_mapa_mapeado[_key_pos_atual()] = { 'lados_bloqueados': [], 'saidas': [] }  
        for s_direcao in obj_coordenadas_monitor.keys():
          if not existe_seta_troca_mapa(s_direcao):
            obj_mapa_mapeado[_key_pos_atual()]['lados_bloqueados'].append(s_direcao)

      # coleta o recurso do mapa
      for caminho in obj_listagem_recursos:  
        s_caminho_recurso = './img' + caminho + '/'
        posicao = checar_imagem_no_mapa(s_caminho_recurso, 0.8, 1, 0.4)
        
        if posicao:
          pyautogui.moveTo(posicao[0] + 5, posicao[1] + 5)
          pyautogui.click()
          time.sleep(10)
  
      # esquema para sair da batalha
      if verifica_personagem_em_batalha():
        if True:
          print('\n--> o personagem está em batalha, entao vamos sair da mesma')
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
        indice_coord_destino += 1
        continue
    
      s_direcao_sugestiva = ''
            
      if X_Y == 'x':
        s_direcao_sugestiva = buscar_nova_direcao('x', i_pos_personagem_x, i_pos_destino_x)
      else:
        s_direcao_sugestiva = buscar_nova_direcao('y', i_pos_personagem_y, i_pos_destino_y)
      
      if s_direcao_sugestiva == '':
        continue
      
      # se existe a seta para trocar de mapa, entao vamos la:
      if existe_seta_troca_mapa(s_direcao_sugestiva):
        print('\n--> direcionando o personagem pra posicao ' + s_direcao_sugestiva)
        i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(s_direcao_sugestiva, i_pos_personagem_x, i_pos_personagem_y)     
        
        pyautogui.click()
        time.sleep(TEMPO_TROCA_MAPA) 
        
      # se nao existir, vamos andar em ambas direcoes diferentes ate encontrar a saida
      # quando encontrar, eu reseto
      else:     
        direcoes_inversas = obj_coordenadas_monitor[s_direcao_sugestiva]['direcoes_inversas']
       
        for direcao in direcoes_inversas:
          while True:
            if existe_seta_troca_mapa(direcao):
              i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(direcao, i_pos_personagem_x, i_pos_personagem_y) 
              
              pyautogui.click()
              time.sleep(TEMPO_TROCA_MAPA)
            
            # quando chegar ao fim da direcao (se existir mapa que isso pode ocorrer), tentamos o processo contrário
            # eu nao sei se é possivel ir tanto pra direita e pra esquerda por exemplo e nao existir a saida pra cima
            # nesse caso, eu trato num futuro se houver.
            else: 
              break        
            
            if existe_seta_troca_mapa(s_direcao_sugestiva):
              i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(s_direcao_sugestiva, i_pos_personagem_x, i_pos_personagem_y) 
              
              indice_coord_destino = 0
              pyautogui.click()
              time.sleep(TEMPO_TROCA_MAPA)
              
main()