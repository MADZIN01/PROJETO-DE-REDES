# === jogo.py ===
# Módulo responsável pela lógica do jogo da velha
# Este arquivo contém todas as funções necessárias para gerenciar o tabuleiro,
# validar jogadas, verificar vitórias e controlar o fluxo do jogo

def criar_tabuleiro():
    """
    Cria e inicializa um tabuleiro vazio 3x3 para o jogo da velha.
    
    Returns:
        list: Matriz 3x3 com espaços vazios (' ') representando casas livres
    
    Exemplo de retorno:
        [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]
    """
    # Cria uma lista de listas 3x3 preenchida com espaços vazios
    return [[' ' for _ in range(3)] for _ in range(3)]

def exibir_tabuleiro(tabuleiro):
    """
    Exibe o tabuleiro formatado no terminal com bordas e numeração.
    
    Args:
        tabuleiro (list): Matriz 3x3 representando o estado atual do jogo
    
    Formato de exibição:
        1   2   3
      +---+---+---+
    1 | X | O |   |
      +---+---+---+
    2 |   | X |   |
      +---+---+---+
    3 | O |   | X |
      +---+---+---+
    """
    # Exibe cabeçalho com numeração das colunas
    print("\n    1   2   3")
    print("  +---+---+---+")
    
    # Itera por cada linha do tabuleiro (0, 1, 2)
    for i in range(3):
        # Inicia linha com número da linha (1-indexado para o usuário)
        linha = f"{i+1} |"
        
        # Adiciona cada célula da linha atual
        for j in range(3):
            # Se a célula está vazia (''), exibe espaço, senão exibe o símbolo (X ou O)
            linha += f" {tabuleiro[i][j] if tabuleiro[i][j] != '' else ' '} |"
        
        # Imprime a linha montada
        print(linha)
        # Imprime separador horizontal entre as linhas
        print("  +---+---+---+")

def realizar_jogada(tabuleiro, linha, coluna, jogador):
    """
    Tenta realizar uma jogada em uma posição específica do tabuleiro.
    
    Args:
        tabuleiro (list): Matriz 3x3 do jogo atual
        linha (int): Linha desejada (0-2, indexação interna)
        coluna (int): Coluna desejada (0-2, indexação interna)  
        jogador (str): Símbolo do jogador ('X' ou 'O')
    
    Returns:
        bool: True se jogada foi realizada com sucesso, False se posição inválida/ocupada
    
    Validações realizadas:
        - Coordenadas dentro dos limites (0-2)
        - Posição não ocupada (contém ' ')
    """
    # Verifica se coordenadas estão dentro dos limites válidos (0-2)
    # E se a posição está livre (contém espaço vazio)
    if 0 <= linha < 3 and 0 <= coluna < 3 and tabuleiro[linha][coluna] == ' ':
        # Posição válida e livre - realiza a jogada
        tabuleiro[linha][coluna] = jogador
        return True
    # Posição inválida ou ocupada - jogada não realizada
    return False

def verificar_vitoria(tabuleiro, jogador):
    """
    Verifica se um jogador específico venceu a partida.
    
    Args:
        tabuleiro (list): Matriz 3x3 do estado atual do jogo
        jogador (str): Símbolo do jogador a ser verificado ('X' ou 'O')
    
    Returns:
        bool: True se o jogador venceu, False caso contrário
    
    Condições de vitória verificadas:
        - 3 símbolos iguais em qualquer linha horizontal
        - 3 símbolos iguais em qualquer coluna vertical  
        - 3 símbolos iguais na diagonal principal (0,0 -> 1,1 -> 2,2)
        - 3 símbolos iguais na diagonal secundária (0,2 -> 1,1 -> 2,0)
    """
    # Verifica todas as linhas e colunas em um loop
    for i in range(3):
        # Verifica linha horizontal i: todas as colunas da linha i
        if all(tabuleiro[i][j] == jogador for j in range(3)):
            return True
        # Verifica coluna vertical i: todas as linhas da coluna i    
        if all(tabuleiro[j][i] == jogador for j in range(3)):
            return True
    
    # Verifica diagonal principal (canto superior esquerdo ao inferior direito)
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] == jogador:
        return True
    
    # Verifica diagonal secundária (canto superior direito ao inferior esquerdo)    
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] == jogador:
        return True
    
    # Nenhuma condição de vitória encontrada
    return False

def verificar_empate(tabuleiro):
    """
    Verifica se o jogo terminou em empate (todas as posições preenchidas sem vencedor).
    
    Args:
        tabuleiro (list): Matriz 3x3 do estado atual do jogo
    
    Returns:
        bool: True se todas as casas estão ocupadas (empate), False se ainda há casas livres
    
    Lógica:
        - Percorre todas as células do tabuleiro
        - Retorna True apenas se NENHUMA célula contém espaço vazio (' ')
        - Esta função deve ser chamada APÓS verificar se há vencedor
    """
    # Verifica se todas as células estão preenchidas (não contêm espaço ' ')
    # Usa list comprehension aninhada para percorrer toda a matriz
    # all() retorna True apenas se TODAS as condições forem True
    return all(cell != ' ' for row in tabuleiro for cell in row)