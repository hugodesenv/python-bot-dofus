class LibCalculo:
  
  @staticmethod
  def calcularProximaCoordenada(pdirecao, xAtual, yAtual):
    if pdirecao == 'direita':
      xAtual += 1
    elif pdirecao == 'esquerda':
      xAtual -= 1
    elif pdirecao == 'baixo':
      yAtual += 1
    elif pdirecao == 'cima':
      yAtual -= 1
      
    return xAtual, yAtual