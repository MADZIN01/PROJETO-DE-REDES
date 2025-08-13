# v0.2 - Comunicação TCP

import socket

PORTA = 12345
BUFFER = 1024
ENCODE = 'utf-8'

def iniciar_host(ip='0.0.0.0', porta=PORTA):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, porta))
    sock.listen(1)
    print(f"[HOST] Aguardando conexão em {ip}:{porta}...")
    conn, addr = sock.accept()
    print(f"[HOST] Conectado com {addr}")
    return conn

def conectar_com_jogador(ip, porta=PORTA):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, porta))
    print(f"[CLIENTE] Conectado ao host em {ip}:{porta}")
    return sock

def enviar_mensagem(sock, mensagem):
    sock.sendall(mensagem.encode(ENCODE))

def receber_mensagem(sock):
    return sock.recv(BUFFER).decode()
