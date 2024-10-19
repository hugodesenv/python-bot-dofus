# definindo bibliotecas
import pyautogui
import os, os.path
import time

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
    'horizontal': 1370,
    'vertical': 35,
    'direcoes_inversas': ['esquerda', 'direita']
  },
  'baixo': {
    'horizontal': 1300,
    'vertical': 890,
    'direcoes_inversas': ['esquerda', 'direita']
  },
  'esquerda': {
    'horizontal': 50,
    'vertical': 400,
    'direcoes_inversas': ['cima', 'baixo']
  },
  'direita': {
    'horizontal': 1800,
    'vertical': 600,
    'direcoes_inversas': ['cima', 'baixo']
  },
}

'''
  exemplo do objeto abaixo:
  obj_mapa_mapeado = [
    [9, -25]{
      lados_bloqueados: ['direita', 'baixo'],
      saidas: [{'x': 10, 'y': 20}, {'x': 2, 'y': -3}]
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

TEMPO_TROCA_MAPA = 8

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

# funcao que verifica se existe a seta de direcionamento no mapa
def existe_seta_troca_mapa(pdirecao):
  x = obj_coordenadas_monitor[pdirecao]['horizontal']
  y = obj_coordenadas_monitor[pdirecao]['vertical'] 
  
  pyautogui.moveTo(x, y, 0.5)  
  
  return checar_imagem_no_mapa('./img/seta/' + pdirecao + '/', 0.4, 2, 1)

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

# com base na direcao, calculamos a nova rota
def buscar_nova_direcao(x_ou_y_str, posicao_atual, posicao_destino):
  orientacao = {'x': ['direita', 'esquerda'], 'y': ['baixo', 'cima']}
  if posicao_destino > posicao_atual:
    return orientacao[x_ou_y_str][0]
  elif posicao_destino < posicao_atual:
    return orientacao[x_ou_y_str][1]
  else:
    return ''
  
# funcao principal
def main():
  # o primeiro passo eh testarmos se esta calculando certo a movimentacao do personagem
  i_pos_personagem_x = int(input('X: '))
  i_pos_personagem_y = int(input('Y: '))

  time.sleep(4)

  #---------------------------------------------------------------------------------------------------------------------
  # primeiro mapeamos o nosso mapa, verificando se ele existe lado que nao pode ser clicavel etc
  # guardando as informacoes no nosso objeto
  def _key_pos_atual(): return (i_pos_personagem_x, i_pos_personagem_y)
  #---------------------------------------------------------------------------------------------------------------------                                                                                      

  # laco principal pra aplicacao nao parar de rodar
  # eu tambem passo dentro do for pra ele percorrer tanto na diagonal quanto na horizontal
  # nessa variavel indice_coord_destino eu guardo o index que estamos indo, e quando chegamos incrementamos + 1
  indice_coord_destino = 0
  
  while True:    
    for X_Y in ['x', 'y']:
      # armazeno o proximo indice destino
      if indice_coord_destino == len(obj_coordenadas_recursos):
        indice_coord_destino = 0
      
      i_pos_destino_x = obj_coordenadas_recursos[indice_coord_destino][0]
      i_pos_destino_y = obj_coordenadas_recursos[indice_coord_destino][1]

      # faz o mapeamento das posiÃ§Ãµes possiveis do mapa atual
      if _key_pos_atual() not in obj_mapa_mapeado:
        obj_mapa_mapeado[_key_pos_atual()] = { 'lados_bloqueados': [], 'saidas': [] }   
        
        for s_direcao in obj_coordenadas_monitor.keys():
          if not existe_seta_troca_mapa(s_direcao):
            obj_mapa_mapeado[_key_pos_atual()]['lados_bloqueados'].append(s_direcao)

      # coleta o recurso do mapa
      for caminho in obj_listagem_recursos:
        s_caminho_recurso = './img' + caminho + '/'
        posicao = checar_imagem_no_mapa(s_caminho_recurso, 0.8, 1, 0)
        if posicao:
          pyautogui.moveTo(posicao[0] + 5, posicao[1] + 5)
          pyautogui.click()
          time.sleep(10)

      # se chegamos no nosso destino, entao buscamos uma nova rota
      if _key_pos_atual() == (i_pos_destino_x, i_pos_destino_y):
        print("\nChegou no nosso destino...")
        indice_coord_destino += 1
        continue

      # descobrimos nossa proxima sugestao de direcao      
      s_direcao_sugestiva = ''
      
      if X_Y == 'x':
        s_direcao_sugestiva = buscar_nova_direcao('x', i_pos_personagem_x, i_pos_destino_x)
      else:
        s_direcao_sugestiva = buscar_nova_direcao('y', i_pos_personagem_y, i_pos_destino_y)
      
      if s_direcao_sugestiva == '':
        print('\nDireção sugestiva está vazia...')
        continue
      
      # se existe a seta para trocar de mapa, entao vamos la:
      if existe_seta_troca_mapa(s_direcao_sugestiva):
        print('\nExiste a seta para trocarmos de mapa...' + s_direcao_sugestiva)
        i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(s_direcao_sugestiva, i_pos_personagem_x, i_pos_personagem_y)     
        
        pyautogui.click()
        time.sleep(TEMPO_TROCA_MAPA) 
      else:        
        # vamos supor que queremos ir para a direita, e o nosso personagem nÃ£o pode ir pra direita porque
        # existe um muro que o impede. Nesse caso, vamos calcular a melhor saÃ­da pro mesmo, sendo assim,
        # primeiro a gente sobe o personagem atÃ© encontrar uma saÃ­da, e depois descemos o personagem atÃ© encontrar uma saÃ­da
        # apos finalizar esses dois processos, voltamos o personagem pra posicao que estava e decidimos o melhor.
        # em alguns casos pode ser que nao exista nem chegando no limite da posiÃ§ao inversa, por exemplo:
        # supondo que eu quero achar a direita, entao tenho que subir, e subir, e subir... mas chega no final do mapa
        # e nada acontece, entao paramos o processo.
        direcoes_inversas = obj_coordenadas_monitor[s_direcao_sugestiva]['direcoes_inversas']
     
        for direcao in direcoes_inversas:
          i = 0
          while True:
            # se encontramos a saida, entao anotamos dentro do objeto
            # eu nunca olho o primeiro por causa do "sentido contrario" que nao funcionaria
            # ja que o personagem possivelmente parou numa saida, entao devemos desconsidera-la
            if i > 0 and existe_seta_troca_mapa(s_direcao_sugestiva):
              print('\nSaida encontrada...')
              obj_mapa_mapeado[_key_pos_atual()]['saidas'].append((i_pos_personagem_x, i_pos_personagem_y))              
              break

            if existe_seta_troca_mapa(direcao):
              i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(direcao, i_pos_personagem_x, i_pos_personagem_y) 
              i += 1
              
              pyautogui.click()
              time.sleep(TEMPO_TROCA_MAPA)
            else: 
              print('\nNada a se fazer!')
              break         
              
        # caso contrÃ¡rio, se nao existir entÃ£o vamos buscar a proxima saÃ­da, com isso guardamos seu posicionamento
        # da posicao atual do personagem para poder voltar posteriormente
        #index_proxima_saida = 0
        
        # para controle de voltar o personagem na posiÃ§Ã£o inicial ao mapear as saidas do mapa
        #i_pos_personagem_inicial_x = i_pos_personagem_x
        #i_pos_personagem_inicial_y = i_pos_personagem_y
        
        # percorremos entao as duas direÃ§oes, pra depois decidir a mais proxima
        # isso Ã© feito apenas se nao conter o mapa mapeado jÃ¡
        #while index_proxima_saida <= 1:
        #  s_nova_direcao = obj_coordenadas_monitor[s_direcao_sugestiva]['direcoes_inversas'][index_proxima_saida]
                
        #  print('\nCalculando nova direÃ§Ã£o: ' + s_nova_direcao)
        #  while ((i_pos_personagem_x != i_pos_personagem_inicial_x) or 
        #         (i_pos_personagem_y != i_pos_personagem_inicial_y)):                  
        #    if existe_seta_troca_mapa(s_nova_direcao):
        #      i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(s_nova_direcao, i_pos_personagem_x, i_pos_personagem_y)     
        #      pyautogui.click()
        #      time.sleep(8)    
    
main()