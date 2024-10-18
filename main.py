# definindo bibliotecas
import pyautogui
import os, os.path
import time

# objeto que armazena o caminho dos itens
obj_listagem_recursos = [
  '/agua',
  '/arvore',
  '/planta/urtiga'
]

# objeto que armazena em qual X e Y o ponteiro do mouse ficará para trocar de mapa:
obj_coordenadas_monitor = {
  'cima': {
    'horizontal': 1300,
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
      saidas: [[10, 2], [1, 3]]
    }
  ]
'''

# objeto que guardamos o mapeamento do nosso mapa atual (lados que nao podem ser clicaveis etc)
obj_mapa_mapeado = {}

TEMPO_TROCA_MAPA = 7

# com base no caminho fornecido, verificamos se a imagem existe no mapa atual
# eu coloquei um delay de 5 segundos quando nao encontrar a imagem pra forçar ele encontrar
def checar_imagem_no_mapa(s_caminho_imagem):
  b_achou = False
  for i in range(5):
    for imagem in os.listdir(s_caminho_imagem):
      try:
        pyautogui.locateOnScreen(s_caminho_imagem + imagem, confidence=0.7)  
        b_achou = True
      except:
        pass
    
    if b_achou: 
      break
    
    time.sleep(1)
    
  return b_achou

# funcao que verifica se existe a seta de direcionamento no mapa
def existe_seta_troca_mapa(pdirecao):
  x = obj_coordenadas_monitor[pdirecao]['horizontal']
  y = obj_coordenadas_monitor[pdirecao]['vertical'] 
  
  pyautogui.moveTo(x, y, 0.5)  
  
  return checar_imagem_no_mapa('./img/seta/' + pdirecao + '/')

# funçao interna para definirmos a movimentação do personagem
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
  
# funcao que faz a coleta dos recursos no mapa atual
def coletar_recurso(p_caminho_imagem):
  s_caminho = './img' + p_caminho_imagem + '/'
  if checar_imagem_no_mapa(s_caminho):
    pyautogui.click()
    time.sleep(6)
    
# funcao principal
def main():
  # o primeiro passo é testarmos se está calculando certo a movimentação do personagem
  i_pos_personagem_x = int(input('X: '))
  i_pos_personagem_y = int(input('Y: '))
  
  i_pos_destino_x = 3
  i_pos_destino_y = -17
  
  b_executando = True
  
  time.sleep(4)

  #---------------------------------------------------------------------------------------------------------------------
  # primeiro mapeamos o nosso mapa, verificando se ele existe lado que nao pode ser clicável etc
  # guardando as informações no nosso objeto
  def _key_pos_atual(): return (i_pos_personagem_x, i_pos_personagem_y)
  #---------------------------------------------------------------------------------------------------------------------                                                                                      
  # funcao anonima para coletar os recursos
  #def _coletar_recursos():
  #  for caminho_imagem in obj_listagem_recursos:
  #    coletar_recurso(caminho_imagem)
  #---------------------------------------------------------------------------------------------------------------------

  # laço principal pra aplicação não parar de rodar
  # eu também passo dentro do for pra ele percorrer tanto na diagonal quanto na horizontal
  while b_executando:    
    for X_Y in ['x', 'y']:
      # faz o mapeamento das posições possiveis do mapa atual
      if _key_pos_atual() not in obj_mapa_mapeado:
        obj_mapa_mapeado[_key_pos_atual()] = { 'lados_bloqueados': [], 'saidas': [] }   
        
        for s_direcao in obj_coordenadas_monitor.keys():
          if not existe_seta_troca_mapa(s_direcao):
            obj_mapa_mapeado[_key_pos_atual()]['lados_bloqueados'].append(s_direcao)

      # se chegamos no nosso destino, então buscamos uma nova rota
      if (_key_pos_atual() == (i_pos_destino_x, i_pos_destino_y)):
        b_executando = False
        break

      # descobrimos nossa proxima sugestao de direcao      
      s_direcao_sugestiva = ''
      
      if X_Y == 'x':
        s_direcao_sugestiva = buscar_nova_direcao('x', i_pos_personagem_x, i_pos_destino_x)
      else:
        s_direcao_sugestiva = buscar_nova_direcao('y', i_pos_personagem_y, i_pos_destino_y)
      
      if s_direcao_sugestiva == '':
        continue
      
      # se existe a seta para trocar de mapa, então vamos lá:
      if existe_seta_troca_mapa(s_direcao_sugestiva):
        i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(s_direcao_sugestiva, i_pos_personagem_x, i_pos_personagem_y)     
        
        pyautogui.click()
        time.sleep(TEMPO_TROCA_MAPA) 
      else:        
        # vamos supor que queremos ir para a direita, e o nosso personagem não pode ir pra direita porque
        # existe um muro que o impede. Nesse caso, vamos calcular a melhor saída pro mesmo, sendo assim,
        # primeiro a gente sobe o personagem até encontrar uma saída, e depois descemos o personagem até encontrar uma saída
        # após finalizar esses dois processos, voltamos o personagem pra posição que estava e decidimos o melhor.
        # em alguns casos pode ser que nao exista nem chegando no limite da posiçao inversa, por exemplo:
        # supondo que eu quero achar a direita, entao tenho que subir, e subir, e subir... mas chega no final do mapa
        # e nada acontece, então paramos o processo.
        direcoes_inversas = obj_coordenadas_monitor[s_direcao_sugestiva]['direcoes_inversas']
     
        for direcao in direcoes_inversas:
          i = 0
          while True:
            # se encontramos a saida, entao anotamos dentro do objeto
            # eu nunca olho o primeiro por causa do "sentido contrario" que nao funcionaria
            # já que o personagem possivelmente parou numa saída, então devemos desconsidera-la
            if i > 0 and existe_seta_troca_mapa(s_direcao_sugestiva):
              #--> apenas tetse @Hugo
              adicionar aqui, dentro do objeto da posiçao atual mapeada
              exemplo...: append((i_pos_personagem_x, i_pos_personagem_y))
              break

            if existe_seta_troca_mapa(direcao):
              i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(direcao, i_pos_personagem_x, i_pos_personagem_y) 
              i += 1
              
              pyautogui.click()
              time.sleep(TEMPO_TROCA_MAPA)
            else: 
              break         
              
        # caso contrário, se nao existir então vamos buscar a proxima saída, com isso guardamos seu posicionamento
        # da posicao atual do personagem para poder voltar posteriormente
        #index_proxima_saida = 0
        
        # para controle de voltar o personagem na posição inicial ao mapear as saidas do mapa
        #i_pos_personagem_inicial_x = i_pos_personagem_x
        #i_pos_personagem_inicial_y = i_pos_personagem_y
        
        # percorremos entao as duas direçoes, pra depois decidir a mais proxima
        # isso é feito apenas se nao conter o mapa mapeado já
        #while index_proxima_saida <= 1:
        #  s_nova_direcao = obj_coordenadas_monitor[s_direcao_sugestiva]['direcoes_inversas'][index_proxima_saida]
                
        #  print('\nCalculando nova direção: ' + s_nova_direcao)
        #  while ((i_pos_personagem_x != i_pos_personagem_inicial_x) or 
        #         (i_pos_personagem_y != i_pos_personagem_inicial_y)):                  
        #    if existe_seta_troca_mapa(s_nova_direcao):
        #      i_pos_personagem_x, i_pos_personagem_y = calcular_troca_mapa(s_nova_direcao, i_pos_personagem_x, i_pos_personagem_y)     
        #      pyautogui.click()
        #      time.sleep(8)    
    
main()