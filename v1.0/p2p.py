# === p2p.py ===
# Módulo de comunicação ponto-a-ponto com suporte a TCP, UDP, IPv4 e IPv6
# Este arquivo implementa todas as funções necessárias para estabelecer comunicação
# de rede entre dois peers (jogadores) usando diferentes protocolos de transporte

import socket

def criar_socket(ip, protocolo):
    """
    Cria um socket apropriado baseado no endereço IP e protocolo especificados.
    
    Args:
        ip (str): Endereço IP (IPv4 ou IPv6) para determinar família do socket
        protocolo (str): Protocolo de transporte ('TCP' ou 'UDP')
    
    Returns:
        socket.socket: Socket configurado com família e tipo corretos
    
    Lógica de detecção:
        - Se IP contém ':', assume IPv6 (AF_INET6)
        - Caso contrário, assume IPv4 (AF_INET)
        - TCP usa SOCK_STREAM (confiável, orientado à conexão)
        - UDP usa SOCK_DGRAM (sem conexão, não confiável)
    """
    # Detecta família do protocolo baseado na presença de ':' no IP
    # IPv6 sempre contém ':', IPv4 nunca contém
    familia = socket.AF_INET6 if ':' in ip else socket.AF_INET
    
    # Define tipo de socket baseado no protocolo de transporte
    tipo = socket.SOCK_STREAM if protocolo == 'TCP' else socket.SOCK_DGRAM
    
    # Cria socket com família e tipo determinados
    sock = socket.socket(familia, tipo)
    
    # CONFIGURAÇÃO ESPECIAL PARA UDP:
    # Permite reutilizar endereço para evitar erro "Address already in use"
    # Necessário porque UDP não tem estado de conexão como TCP
    if protocolo == 'UDP':
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    return sock

def aguardar_conexao(protocolo, ip, porta):
    """
    Modo servidor: aguarda conexão TCP ou primeiro pacote UDP de um cliente.
    
    Args:
        protocolo (str): 'TCP' ou 'UDP'
        ip (str): IP local para bind (use '0.0.0.0' para aceitar de qualquer IP)
        porta (int): Porta local para escutar
    
    Returns:
        tuple: (socket_conectado, endereco_remoto) ou (None, None) em caso de erro
    
    Comportamento por protocolo:
        TCP: Faz bind/listen/accept e retorna conexão estabelecida
        UDP: Faz bind e aguarda primeiro pacote para identificar cliente
    """
    # Cria socket apropriado para IP e protocolo especificados
    s = criar_socket(ip, protocolo)
    
    try:
        # BIND: Associa socket ao endereço local
        if s.family == socket.AF_INET6:
            # IPv6 requer 4 parâmetros: (ip, porta, flow_info, scope_id)
            s.bind((ip, porta, 0, 0))
        else:
            # IPv4 requer apenas 2 parâmetros: (ip, porta)
            s.bind((ip, porta))
        
        if protocolo == 'TCP':
            # === MODO TCP (ORIENTADO À CONEXÃO) ===
            
            # Listen: Coloca socket em modo de escuta (máximo 1 conexão pendente)
            s.listen(1)
            print(f"Aguardando conexão TCP em {ip}:{porta}...")
            
            # Accept: Bloqueia até receber conexão de cliente
            conn, addr = s.accept()
            print(f"Conectado com {addr}")
            
            # Fecha socket servidor (só precisamos da conexão estabelecida)
            s.close()
            
            # Retorna conexão estabelecida e None (endereço já conhecido)
            return conn, None
            
        else:
            # === MODO UDP (SEM CONEXÃO) ===
            
            print(f"Aguardando primeiro pacote UDP em {ip}:{porta}...")
            
            # RecvFrom: Aguarda primeiro pacote para descobrir endereço do cliente
            # UDP não tem "conexão", então identificamos cliente pelo primeiro pacote
            try:
                data, addr = s.recvfrom(1024)  # Buffer de 1024 bytes
                print(f"Primeiro pacote UDP recebido de {addr}: {data.decode()}")
                
                # CONFIRMAÇÃO DE CONEXÃO UDP:
                # Envia resposta para confirmar que recebeu o pacote inicial
                s.sendto("CONEXAO_CONFIRMADA".encode(), addr)
                print(f"Confirmação enviada para {addr}")
                
                # Retorna socket (para comunicação futura) e endereço do cliente
                return s, addr
                
            except Exception as e:
                print(f"Erro recebendo primeiro pacote UDP: {e}")
                s.close()
                return None, None
                
    except Exception as e:
        print(f"Erro ao fazer bind/listen: {e}")
        s.close()
        return None, None

def conectar_cliente(protocolo, ip, porta):
    """
    Modo cliente: conecta-se a um servidor TCP ou estabelece comunicação UDP.
    
    Args:
        protocolo (str): 'TCP' ou 'UDP'
        ip (str): IP do servidor/host
        porta (int): Porta do servidor/host
    
    Returns:
        tuple: (socket, endereco_servidor) ou (None, None) em caso de erro
    
    Comportamento por protocolo:
        TCP: Estabelece conexão three-way handshake
        UDP: Envia pacote inicial e aguarda confirmação do servidor
    """
    # Cria socket apropriado para comunicação
    s = criar_socket(ip, protocolo)
    
    if protocolo == 'TCP':
        # === MODO TCP (ESTABELECE CONEXÃO) ===
        try:
            # Connect: Inicia three-way handshake TCP com servidor
            s.connect((ip, porta))
            print(f"Conectado ao servidor TCP {ip}:{porta}")
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            s.close()
            return None, None
            
        # Retorna socket conectado e None (conexão já estabelecida)
        return s, None
        
    else:
        # === MODO UDP (SEM CONEXÃO - HANDSHAKE MANUAL) ===
        
        print(f"Cliente UDP pronto para se comunicar com {ip}:{porta}")
        endereco_servidor = (ip, porta)
        
        try:
            # HANDSHAKE UDP CUSTOMIZADO:
            # Como UDP não tem conexão, implementamos handshake manual
            
            # 1. Envia pacote inicial para servidor saber nosso endereço
            s.sendto("CONEXAO_UDP".encode(), endereco_servidor)
            print("Pacote inicial UDP enviado, aguardando confirmação...")
            
            # 2. Aguarda confirmação do servidor (timeout de 10 segundos)
            s.settimeout(10.0)
            data, addr = s.recvfrom(1024)
            
            # 3. Verifica se recebeu confirmação esperada
            if data.decode() == "CONEXAO_CONFIRMADA":
                print(f"Conexão UDP confirmada com {addr}")
                # Remove timeout para comunicação normal
                s.settimeout(None)
            else:
                print(f"Resposta inesperada do servidor: {data.decode()}")
                
        except socket.timeout:
            print("Timeout aguardando confirmação do servidor")
            s.close()
            return None, None
        except Exception as e:
            print(f"Erro ao estabelecer conexão UDP: {e}")
            s.close()
            return None, None
            
        # Retorna socket e endereço do servidor para comunicação futura
        return s, endereco_servidor

def enviar(sock, msg, protocolo, endereco=None):
    """
    Envia uma mensagem através do socket usando o protocolo especificado.
    
    Args:
        sock (socket): Socket para envio
        msg (str): Mensagem a ser enviada
        protocolo (str): 'TCP' ou 'UDP'
        endereco (tuple, optional): Endereço destino (obrigatório para UDP)
    
    Returns:
        bool: True se envio foi bem-sucedido, False em caso de erro
    
    Diferenças por protocolo:
        TCP: Usa send() - endereço já conhecido pela conexão
        UDP: Usa sendto() - precisa especificar endereço a cada envio
    """
    try:
        if protocolo == 'TCP':
            # TCP: Send simples (conexão já estabelecida conhece o destino)
            # Codifica string para bytes antes do envio
            sock.send(msg.encode())
        else:
            # UDP: SendTo com endereço específico (necessário a cada envio)
            if endereco is None:
                print("ERRO: Endereço necessário para UDP")
                return False
            # Envia para endereço específico codificando mensagem para bytes
            sock.sendto(msg.encode(), endereco)
            
        return True
        
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return False

def receber(sock, protocolo):
    """
    Recebe uma mensagem através do socket usando o protocolo especificado.
    
    Args:
        sock (socket): Socket para recebimento
        protocolo (str): 'TCP' ou 'UDP'
    
    Returns:
        tuple: (mensagem_decodificada, endereco_remetente) ou (None, None) em caso de erro
    
    Diferenças por protocolo:
        TCP: Usa recv() - retorna apenas dados (endereço já conhecido)
        UDP: Usa recvfrom() - retorna dados E endereço do remetente
    
    Timeout: 30 segundos para UDP, sem timeout para TCP
    """
    try:
        if protocolo == 'TCP':
            # TCP: Recebe dados da conexão estabelecida
            data = sock.recv(1024)  # Buffer de 1024 bytes
            
            # Verifica se conexão foi fechada pelo peer
            if not data:
                return None, None  # Conexão fechada
                
            # Decodifica bytes para string e retorna
            return data.decode(), None
            
        else:
            # UDP: Recebe dados com informação do remetente
            
            # Timeout de 30 segundos para evitar travamento infinito
            sock.settimeout(30.0)
            
            # RecvFrom retorna dados E endereço do remetente
            data, addr = sock.recvfrom(1024)
            
            # Decodifica e retorna mensagem com endereço do remetente
            return data.decode(), addr
            
    except socket.timeout:
        print("Timeout recebendo dados")
        return None, None
    except Exception as e:
        print(f"Erro ao receber mensagem: {e}")
        return None, None

def encerrar(sock):
    """
    Fecha o socket com segurança, tratando possíveis exceções.
    
    Args:
        sock (socket): Socket a ser fechado
    
    Importância:
        - Libera recursos do sistema operacional
        - Evita problemas de "Address already in use"
        - Boa prática de programação de rede
        
    Tratamento de erro:
        - Usa try/except para evitar crashes se socket já foi fechado
        - Função sempre executa sem gerar exceções
    """
    try:
        if sock:  # Verifica se socket existe e não é None
            sock.close()  # Fecha socket e libera recursos
    except:
        # Ignora qualquer erro (socket pode já estar fechado)
        # Usado bare except para máxima compatibilidade
        pass