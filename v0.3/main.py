# v0.3 - main.py (Suporte TCP e UDP)

from jogo import exibir_tabuleiro, verificar_vitoria, tabuleiro
from p2p import iniciar_host, conectar_com_jogador, enviar_mensagem, receber_mensagem

protocolo = input("Protocolo (TCP/UDP): ").strip().upper()
modo = input("Você é o host (h) ou cliente (c)? ").strip().lower()
porta = 12345

if modo == 'h':
    ip = input("Digite o IP para escutar (0.0.0.0 para todas interfaces): ").strip()
    conexao, ip_destino, porta_destino = iniciar_host(protocolo, ip, porta)
    meu_turno = True
    minha_marca = 'X'
else:
    ip = input("Digite o IP do host: ").strip()
    conexao, ip_destino, porta_destino = conectar_com_jogador(protocolo, ip, porta)
    meu_turno = False
    minha_marca = 'O'

rodando = True
jogadas = 0

while rodando:
    exibir_tabuleiro()

    if meu_turno:
        try:
            linha = int(input("Linha (0–2): "))
            coluna = int(input("Coluna (0–2): "))
            if tabuleiro[linha][coluna] != " ":
                print("Posição ocupada!")
                continue
        except:
            print("Entrada inválida.")
            continue

        tabuleiro[linha][coluna] = minha_marca
        enviar_mensagem(conexao, f"{linha},{coluna}", protocolo, ip_destino, porta_destino)
        jogadas += 1

        if verificar_vitoria(minha_marca):
            exibir_tabuleiro()
            print(f"Jogador {minha_marca} venceu!")
            break
        elif jogadas == 9:
            exibir_tabuleiro()
            print("Empate!")
            break
    else:
        print("Aguardando jogada do oponente...")
        mensagem, _, _ = receber_mensagem(conexao, protocolo)
        linha, coluna = map(int, mensagem.split(","))
        tabuleiro[linha][coluna] = 'X' if minha_marca == 'O' else 'O'
        jogadas += 1

        if verificar_vitoria('X' if minha_marca == 'O' else 'O'):
            exibir_tabuleiro()
            print("Jogador adversário venceu!")
            break
        elif jogadas == 9:
            exibir_tabuleiro()
            print("Empate!")
            break

    meu_turno = not meu_turno

print("Jogo encerrado.")
