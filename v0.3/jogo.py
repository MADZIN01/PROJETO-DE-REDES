# v0.2 - Jogo da Velha (Módulo de jogo)

tabuleiro = [[" " for _ in range(3)] for _ in range(3)]

def exibir_tabuleiro():
    print("   0   1   2")
    for i, linha in enumerate(tabuleiro):
        print(f"{i}  {' | '.join(linha)}")
        if i < 2:
            print("  ---+---+---")

def verificar_vitoria(j):
    for i in range(3):
        if tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] == j:
            return True
        if tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] == j:
            return True
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] == j:
        return True
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] == j:
        return True
    return False
