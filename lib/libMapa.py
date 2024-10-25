import pyautogui
import cv2
import numpy as np
import os, os.path

class LibMapa:
  @staticmethod
  def obterPontoDaImagem(imagem_a_comparar):
    # Capturar a tela com o pyautogui
    screen_shot = pyautogui.screenshot()

    # Converter a captura de tela para um array NumPy (necessário para usar com OpenCV)
    screen_shot = np.array(screen_shot)

    # Carregar a imagem de origem que será usada no template matching
    imagem_origem = cv2.imread(imagem_a_comparar)

    # Converter as imagens para escala de cinza
    screen_shot_cinza = cv2.cvtColor(screen_shot, cv2.COLOR_BGR2GRAY)
    imagem_origem_cinza = cv2.cvtColor(imagem_origem, cv2.COLOR_BGR2GRAY)

    # Aplicar equalização de histograma para normalizar as imagens
    screen_shot_cinza = cv2.equalizeHist(screen_shot_cinza)
    imagem_origem_cinza = cv2.equalizeHist(imagem_origem_cinza)

    # Aplicar template matching
    result = cv2.matchTemplate(screen_shot_cinza, imagem_origem_cinza, cv2.TM_CCOEFF_NORMED)

    # Encontrar o local com maior correspondência
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.7  # Por exemplo, confiança de 70%

    if max_val >= threshold:
      # O ponto máximo (max_loc) contém as coordenadas (left, top)
      left, top = max_loc
      return left, top
    else:
      return -1, -1
    
  @staticmethod
  def buscarNovaDirecao(x_ou_y_str, posicao_atual, posicao_destino):
    orientacao = {'x': ['direita', 'esquerda'], 'y': ['baixo', 'cima']}
    
    if posicao_destino > posicao_atual:
      return orientacao[x_ou_y_str][0]
    elif posicao_destino < posicao_atual:
      return orientacao[x_ou_y_str][1]
    else:
      return ''
    
  # com base num diretorio de imagens, verificamos se ela existe no mapa atual
  @staticmethod
  def verificaImagemExiste(pCaminhoImagem):
    x, y = -1, -1
        
    for imagem in os.listdir(pCaminhoImagem):
      try:
        # Obtém a posição da imagem
        x, y = LibMapa.obterPontoDaImagem(pCaminhoImagem + '/' + imagem)
                
        if x > 0 or y > 0:
          # Captura a posição atual do mouse quando a imagem é encontrada
          mouse_x, mouse_y = pyautogui.position()
          return x, y, mouse_x, mouse_y  # Retorna a posição da imagem e do mouse       
      except:
        pyautogui.sleep(1)
        pass
       
    return x, y, -1, -1  