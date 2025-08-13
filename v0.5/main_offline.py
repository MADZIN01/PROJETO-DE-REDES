
from jogo import criar_tabuleiro, exibir_tabuleiro, verificar_vitoria, verificar_empate

def main():
    tabuleiro = criar_tabuleiro()
    jogador = "X"

    while True:
        exibir_tabuleiro(tabuleiro)
        print(f"Vez do jogador {jogador}")
        try:
            linha = int(input("Linha (0-2): "))
            coluna = int(input("Coluna (0-2): "))
        except ValueError:
            print("Entrada inválida.")
            continue

        if not (0 <= linha <= 2 and 0 <= coluna <= 2):
            print("Posição fora do tabuleiro.")
            continue

        if tabuleiro[linha][coluna] != " ":
            print("Posição ocupada.")
            continue

        tabuleiro[linha][coluna] = jogador

        if verificar_vitoria(tabuleiro, jogador):
            exibir_tabuleiro(tabuleiro)
            print(f"Jogador {jogador} venceu!")
            break
        elif verificar_empate(tabuleiro):
            exibir_tabuleiro(tabuleiro)
            print("Empate!")
            break

        jogador = "O" if jogador == "X" else "X"

if __name__ == "__main__":
    main()
