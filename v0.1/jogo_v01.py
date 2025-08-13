import os
os.system("title MADZIN01 - v0.1.1")
# jogo_offline.py
# Função que cria o tabuleiro 3x3 vazio
def criar_tabuleiro():
    return [[" " for _ in range(3)] for _ in range(3)]

# Função que imprime o tabuleiro formatado no terminal

# ...existing code...
def exibir_tabuleiro(tab):
    print("   0   1   2")
    for i, linha in enumerate(tab):
        print(f"{i}  " + " | ".join(linha))
        if i < 2:
            print("  ---+---+---")
# ...existing code...

# Verifica se o jogador atual venceu
def verificar_vitoria(tab, jogador):
    # Verifica linhas e colunas
    for i in range(3):
        if all([tab[i][j] == jogador for j in range(3)]):  # Linha i
            return True
        if all([tab[j][i] == jogador for j in range(3)]):  # Coluna i
            return True
    # Verifica diagonais
    if all([tab[i][i] == jogador for i in range(3)]):  # Diagonal principal
        return True
    if all([tab[i][2 - i] == jogador for i in range(3)]):  # Diagonal secundária
        return True
    return False

# Verifica se todas as casas estão preenchidas sem vencedor
def verificar_empate(tab):
    return all([cell != " " for row in tab for cell in row])

# Função principal do jogo
def jogar():
    tabuleiro = criar_tabuleiro()  # Inicia tabuleiro vazio
    turno = "X"  # Jogador "X" começa

    while True:
        exibir_tabuleiro(tabuleiro)
        print(f"Turno do jogador {turno}")

        # Solicita entrada do jogador
        try:
            linha = int(input("Linha (0, 1, 2): "))
            coluna = int(input("Coluna (0, 1, 2): "))
        except ValueError:
            print("Entrada inválida. Use apenas números.")
            continue

        # Verifica se a jogada está dentro do tabuleiro
        if linha not in range(3) or coluna not in range(3):
            print("Posição fora do tabuleiro.")
            continue

        # Verifica se a posição já está ocupada
        if tabuleiro[linha][coluna] != " ":
            print("Espaço já ocupado.")
            continue

        # Marca a jogada no tabuleiro
        tabuleiro[linha][coluna] = turno

        # Verifica vitória
        if verificar_vitoria(tabuleiro, turno):
            exibir_tabuleiro(tabuleiro)
            print(f"Jogador {turno} venceu!")
            break
        # Verifica empate
        elif verificar_empate(tabuleiro):
            exibir_tabuleiro(tabuleiro)
            print("Empate!")
            break

        # Troca o turno
        turno = "O" if turno == "X" else "X"

# Executa o jogo apenas se o arquivo for rodado diretamente
if __name__ == "__main__":
    jogar()
