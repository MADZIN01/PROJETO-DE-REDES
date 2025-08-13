# v0.5 - Comunicação TCP/UDP

import socket

PORTA_PADRAO = 12345
BUFFER = 1024
ENCODE = 'utf-8'

def criar_socket(protocolo):
    tipo = socket.SOCK_STREAM if protocolo == "TCP" else socket.SOCK_DGRAM
    return socket.socket(socket.AF_INET, tipo)

def iniciar_host(protocolo, ip, porta=PORTA_PADRAO):
    protocolo = protocolo.upper()
    sock = criar_socket(protocolo)
    sock.bind((ip, porta))

    if protocolo == "TCP":
        sock.listen(1)
        print(f"[HOST] Aguardando conexão TCP em {ip}:{porta}...")
        conn, addr = sock.accept()
        print(f"[HOST] Conectado com {addr}")
        return conn, None, None
    else:
        print(f"[HOST] Aguardando jogada via UDP em {ip}:{porta}...")
        dados, addr = sock.recvfrom(BUFFER)
        print(f"[HOST] Recebeu de: {addr}")
        return sock, addr[0], addr[1]

def conectar_com_jogador(protocolo, ip, porta=PORTA_PADRAO):
    protocolo = protocolo.upper()
    sock = criar_socket(protocolo)

    if protocolo == "TCP":
        sock.connect((ip, porta))
        print(f"[CLIENTE] Conectado ao host TCP em {ip}:{porta}")
        return sock, None, None
    else:
        print(f"[CLIENTE] Preparado para enviar via UDP para {ip}:{porta}")
        return sock, ip, porta

def enviar_mensagem(sock, mensagem, protocolo, ip_destino=None, porta_destino=None):
    if protocolo == "TCP":
        sock.sendall(mensagem.encode(ENCODE))
    else:
        if not ip_destino or not porta_destino:
            raise ValueError("IP e porta do destino são obrigatórios para UDP.")
        sock.sendto(mensagem.encode(ENCODE), (ip_destino, porta_destino))

def receber_mensagem(sock, protocolo):
    if protocolo == "TCP":
        return sock.recv(BUFFER).decode(), None, None
    else:
        dados, addr = sock.recvfrom(BUFFER)
        return dados.decode(), addr[0], addr[1]
