# === main.py ===
# Interface principal da aplicação (Jogo da Velha offline e online)
# Este arquivo coordena a interação entre usuário, lógica do jogo e comunicação de rede
# Implementa o protocolo de aplicação para comunicação P2P entre jogadores

import os
from jogo import criar_tabuleiro, exibir_tabuleiro, realizar_jogada, verificar_vitoria, verificar_empate
from p2p import aguardar_conexao, conectar_cliente, enviar, receber, encerrar

# ===================================================================
# PROTOCOLO DE APLICAÇÃO - DEFINIÇÃO DAS MENSAGENS
# ===================================================================
# Define formato padrão para comunicação entre jogadores:
# Formato: TIPO|PARAMETRO1|PARAMETRO2|...
# Permite interpretação consistente das mensagens trocadas

def criar_msg_jogada(linha, coluna):
    """
    Cria mensagem padronizada para transmitir uma jogada.
    
    Args:
        linha (int): Linha da jogada (0-2)
        coluna (int): Coluna da jogada (0-2)
    
    Returns:
        str: Mensagem no formato "JOGADA|linha|coluna"
    
    Exemplo: "JOGADA|1|2" (jogada na linha 1, coluna 2)
    """
    return f"JOGADA|{linha}|{coluna}"

def criar_msg_fim(vencedor):
    """
    Cria mensagem para indicar fim de jogo com vencedor.
    
    Args:
        vencedor (str): Símbolo do jogador vencedor ('X' ou 'O')
    
    Returns:
        str: Mensagem no formato "FIM_DE_JOGO|vencedor"
    
    Exemplo: "FIM_DE_JOGO|X" (jogador X venceu)
    """
    return f"FIM_DE_JOGO|{vencedor}"

def criar_msg_empate():
    """
    Cria mensagem para indicar empate no jogo.
    
    Returns:
        str: Mensagem "EMPATE"
    
    Usado quando tabuleiro está cheio sem vencedor
    """
    return "EMPATE"

def interpretar_msg(msg):
    """
    Interpreta mensagem recebida e extrai informações relevantes.
    
    Args:
        msg (str): Mensagem recebida do oponente
    
    Returns:
        tuple: Tupla com tipo de mensagem e parâmetros extraídos
    
    Tipos de mensagem suportados:
        - "JOGADA|linha|coluna" -> ("JOGADA", linha_int, coluna_int)
        - "FIM_DE_JOGO|vencedor" -> ("FIM_DE_JOGO", vencedor_str)
        - "EMPATE" -> ("EMPATE",)
        - Mensagem inválida -> ("ERRO",)
    """
    # Remove espaços em branco e divide mensagem por '|'
    partes = msg.strip().split('|')
    tipo = partes[0]  # Primeiro elemento é sempre o tipo

    if tipo == "JOGADA":
        # Extrai coordenadas e converte para inteiros
        linha = int(partes[1])
        coluna = int(partes[2])
        return tipo, linha, coluna
        
    elif tipo == "FIM_DE_JOGO":
        # Extrai símbolo do vencedor
        return tipo, partes[1]
        
    elif tipo == "EMPATE":
        # Empate não tem parâmetros adicionais
        return tipo,
        
    else:
        # Mensagem não reconhecida
        return "ERRO",

def limpar_tela():
    """
    Limpa a tela do terminal de forma multiplataforma.
    
    Detecta sistema operacional e usa comando apropriado:
        - Windows: 'cls'
        - Unix/Linux/Mac: 'clear'
    
    Melhora experiência do usuário mantendo interface limpa
    """
    # os.name retorna 'nt' para Windows, outros valores para Unix-like
    os.system('cls' if os.name == 'nt' else 'clear')

def jogar_offline():
    """
    Implementa modo de jogo offline para dois jogadores no mesmo computador.
    
    Fluxo do jogo:
        1. Cria tabuleiro vazio
        2. Alterna entre jogadores X e O
        3. Solicita coordenadas de jogada
        4. Valida e executa jogada
        5. Verifica condições de vitória/empate
        6. Continua até fim de jogo
    
    Características:
        - Interface de linha de comando
        - Validação de entrada do usuário
        - Alternância automática de jogadores
        - Verificação de condições de fim de jogo
    """
    # Inicializa estado do jogo
    tabuleiro = criar_tabuleiro()
    jogador_atual = 'X'  # X sempre começa

    # Loop principal do jogo
    while True:
        # Atualiza interface
        limpar_tela()
        print("Jogo da Velha - Modo Offline")
        exibir_tabuleiro(tabuleiro)
        print(f"Vez do jogador {jogador_atual}")

        # Solicita entrada do jogador com tratamento de erro
        try:
            # Converte entrada 1-3 para índices 0-2
            linha = int(input("Linha (1-3): ")) - 1
            coluna = int(input("Coluna (1-3): ")) - 1
        except ValueError:
            # Trata entrada não numérica
            print("Entrada inválida!")
            continue

        # Tenta realizar jogada
        if realizar_jogada(tabuleiro, linha, coluna, jogador_atual):
            # Jogada válida - verifica condições de fim
            
            if verificar_vitoria(tabuleiro, jogador_atual):
                # Vitória detectada
                limpar_tela()
                exibir_tabuleiro(tabuleiro)
                print(f"Jogador {jogador_atual} venceu!")
                break
                
            elif verificar_empate(tabuleiro):
                # Empate detectado
                limpar_tela()
                exibir_tabuleiro(tabuleiro)
                print("Empate!")
                break
                
            # Jogo continua - alterna jogador
            jogador_atual = 'O' if jogador_atual == 'X' else 'X'
            
        else:
            # Jogada inválida - solicita nova entrada
            print("Posição inválida! Tente novamente.")
            input("ENTER para continuar...")

def jogar_online():
    """
    Implementa modo de jogo online P2P entre dois jogadores em computadores diferentes.
    
    Funcionalidades:
        - Seleção de protocolo (TCP/UDP)
        - Modo host ou cliente
        - Comunicação P2P usando protocolo personalizado
        - Sincronização de jogadas entre jogadores
        - Tratamento de desconexões
    
    Fluxo de execução:
        1. Configura parâmetros de rede (protocolo, IP, porta)
        2. Estabelece conexão (host aguarda, cliente conecta)
        3. Executa loop de jogo com alternância de turnos
        4. Sincroniza jogadas via rede
        5. Trata mensagens de fim de jogo
    """
    # === CONFIGURAÇÃO INICIAL ===
    
    # Solicita parâmetros de rede do usuário
    protocolo = input("Protocolo (TCP/UDP): ").strip().upper()
    modo = input("Você é host ou cliente? (h/c): ").strip().lower()
    
    # Instruções para configuração de IP
    print("SE VOCÊ FOR O HOST USE : 0.0.0.0")
    print("SE VOCÊ É O CLIENTE DIGITE O IP DO HOST : ")
    ip = input("IP do peer: ").strip()
    
    print("PORTA : 5555")
    porta = int(input("Porta: "))

    # === INICIALIZAÇÃO DO JOGO ===
    
    # Inicializa estado do jogo
    tabuleiro = criar_tabuleiro()
    
    # Define papel do jogador local baseado no modo
    jogador_local = 'X' if modo == 'h' else 'O'  # Host é sempre X, cliente é O
    minha_vez = modo == 'h'  # Host começa jogando
    
    # Variáveis de comunicação
    sock = None
    endereco_remoto = None

    # === ESTABELECIMENTO DE CONEXÃO ===
    
    if modo == 'h':
        # MODO HOST: Aguarda conexão do cliente
        sock, endereco_remoto = aguardar_conexao(protocolo, ip, porta)
        if sock is None:
            print("Falha ao estabelecer conexão")
            return
    else:
        # MODO CLIENTE: Conecta ao host
        sock, endereco_remoto = conectar_cliente(protocolo, ip, porta)
        if sock is None:
            print("Falha ao conectar")
            return

    print("Conexão estabelecida! Iniciando jogo...")
    input("Pressione ENTER para começar...")

    # === LOOP PRINCIPAL DO JOGO ONLINE ===
    
    while True:
        # Atualiza interface
        limpar_tela()
        print("Jogo da Velha - Modo Online")
        exibir_tabuleiro(tabuleiro)

        if minha_vez:
            # === TURNO LOCAL: Jogador atual faz jogada ===
            
            print(f"Sua vez ({jogador_local})")
            
            # Solicita jogada com tratamento de erro
            try:
                linha = int(input("Linha (1-3): ")) - 1
                coluna = int(input("Coluna (1-3): ")) - 1
            except ValueError:
                print("Entrada inválida!")
                continue

            # Valida e executa jogada local
            if realizar_jogada(tabuleiro, linha, coluna, jogador_local):
                # Jogada válida - transmite para oponente
                if not enviar(sock, criar_msg_jogada(linha, coluna), protocolo, endereco_remoto):
                    print("Erro ao enviar jogada")
                    break
                    
                # Verifica condições de fim após jogada local
                if verificar_vitoria(tabuleiro, jogador_local):
                    # Vitória local - notifica oponente
                    enviar(sock, criar_msg_fim(jogador_local), protocolo, endereco_remoto)
                    limpar_tela()
                    exibir_tabuleiro(tabuleiro)
                    print("Você venceu!")
                    break
                    
                elif verificar_empate(tabuleiro):
                    # Empate - notifica oponente
                    enviar(sock, criar_msg_empate(), protocolo, endereco_remoto)
                    limpar_tela()
                    exibir_tabuleiro(tabuleiro)
                    print("Empate!")
                    break
                    
                # Jogo continua - passa turno para oponente
                minha_vez = False
                
            else:
                # Jogada inválida - solicita nova entrada
                print("Posição inválida!")
                input("ENTER para continuar...")
                
        else:
            # === TURNO REMOTO: Aguarda jogada do oponente ===
            
            print("Aguardando jogada do oponente...")
            
            # Recebe mensagem do oponente
            msg, addr = receber(sock, protocolo)
                
            if msg is None:
                # Erro na comunicação ou timeout
                print("Erro na comunicação ou timeout")
                break
                
            # Para UDP, armazena endereço do remetente se ainda não conhecido
            if protocolo == 'UDP' and endereco_remoto is None:
                endereco_remoto = addr
                
            # Interpreta mensagem recebida
            dados = interpretar_msg(msg)
            tipo = dados[0]

            if tipo == "JOGADA":
                # === PROCESSAMENTO DE JOGADA REMOTA ===
                
                _, linha, coluna = dados  # Extrai coordenadas
                jogador_remoto = 'O' if jogador_local == 'X' else 'X'
                
                # Executa jogada do oponente no tabuleiro local
                if realizar_jogada(tabuleiro, linha, coluna, jogador_remoto):
                    # Jogada válida - passa turno de volta para jogador local
                    minha_vez = True
                else:
                    print("Jogada inválida recebida do oponente!")
                    
            elif tipo == "FIM_DE_JOGO":
                # === PROCESSAMENTO DE FIM DE JOGO ===
                
                vencedor = dados[1]
                limpar_tela()
                exibir_tabuleiro(tabuleiro)
                
                # Verifica se jogador local venceu ou perdeu
                if vencedor != jogador_local:
                    print("Você perdeu!")
                else:
                    print("Você venceu!")
                break
                
            elif tipo == "EMPATE":
                # === PROCESSAMENTO DE EMPATE ===
                
                limpar_tela()
                exibir_tabuleiro(tabuleiro)
                print("Empate!")
                break
                
            else:
                # === MENSAGEM NÃO RECONHECIDA ===
                print(f"Mensagem desconhecida recebida: {msg}")

    # === FINALIZAÇÃO ===
    
    # Fecha conexão de forma segura
    encerrar(sock)
    input("Pressione ENTER para sair...")

def main():
    """
    Função principal da aplicação - implementa menu principal e coordena execução.
    
    Funcionalidades:
        - Menu interativo para seleção de modo de jogo
        - Loop infinito até usuário escolher sair
        - Tratamento de opções inválidas
        - Limpeza de tela para melhor experiência
    
    Opções disponíveis:
        1. Jogar offline (dois jogadores no mesmo computador)
        2. Jogar online (dois jogadores em computadores diferentes via rede)
        3. Sair da aplicação
    
    Design pattern: Menu loop com dispatch para funções específicas
    """
    # Loop principal da aplicação
    while True:
        # === EXIBIÇÃO DO MENU PRINCIPAL ===
        
        limpar_tela()
        print("============================")
        print("     JOGO DA VELHA     ")
        print("============================")
        print("1. Jogar offline")
        print("2. Jogar online")
        print("3. Sair")
        
        # Solicita escolha do usuário
        escolha = input("Escolha uma opção: ")

        # === PROCESSAMENTO DA ESCOLHA ===
        
        if escolha == '1':
            # Modo offline: jogo local entre dois jogadores
            jogar_offline()
            
        elif escolha == '2':
            # Modo online: jogo em rede P2P
            jogar_online()
            
        elif escolha == '3':
            # Encerra aplicação
            break
            
        else:
            # Opção inválida - exibe erro e retorna ao menu
            print("Opção inválida!")
            input("ENTER para continuar...")

# === PONTO DE ENTRADA DA APLICAÇÃO ===

if __name__ == '__main__':
    """
    Ponto de entrada padrão do Python.
    
    Garante que main() só execute quando arquivo é executado diretamente,
    não quando importado como módulo por outro arquivo.
    
    Boa prática em Python para aplicações executáveis.
    """
    main()
