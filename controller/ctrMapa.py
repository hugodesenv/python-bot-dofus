import os, os.path
from lib.libMapa import *

class CtrMapa:
  def verificaImagemExiste(self, pCaminhoImagem):
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