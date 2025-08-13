import tkinter as tk
from tkinter import messagebox
import threading

# Importações do seu projeto original
from jogo import criar_tabuleiro, exibir_tabuleiro, realizar_jogada, verificar_vitoria, verificar_empate
from p2p import aguardar_conexao, conectar_cliente, enviar, receber, encerrar

class JogoDaVelhaGUI:
    """
    Classe principal da interface gráfica do Jogo da Velha.
    
    Integra funcionalidades offline e online com interface Tkinter.
    Mantém toda a lógica de rede do projeto original, adaptada para GUI.
    
    Atributos:
        root: Janela principal do Tkinter
        tabuleiro: Matriz 3x3 representando o estado do jogo
        jogador_atual: Símbolo do jogador atual ('X' ou 'O')
        modo_jogo: Tipo de jogo ('pvp', 'online')
        botoes_tabuleiro: Matriz de botões da interface gráfica
        
        # Variáveis específicas do modo online
        sock: Socket de comunicação
        endereco_remoto: Endereço do oponente
        jogador_local: Símbolo do jogador local ('X' ou 'O')
        minha_vez: Boolean indicando se é a vez do jogador local
        conexao_ativa: Boolean indicando se conexão está estabelecida
    """
    
    def __init__(self):
        """
        Inicializa a interface gráfica e variáveis do jogo.
        
        Configura:
        - Janela principal com tamanho fixo
        - Variáveis de estado do jogo
        - Variáveis específicas para modo online
        - Inicia com o menu principal
        """
        # === CONFIGURAÇÃO DA JANELA PRINCIPAL ===
        self.root = tk.Tk()
        self.root.title("Jogo da Velha")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # === VARIÁVEIS DE ESTADO DO JOGO ===
        self.tabuleiro = [["" for _ in range(3)] for _ in range(3)]
        self.jogador_atual = "X"
        self.modo_jogo = None
        self.botoes_tabuleiro = []
        
        # === VARIÁVEIS ESPECÍFICAS DO MODO ONLINE ===
        # Comunicação de rede
        self.sock = None
        self.endereco_remoto = None
        
        # Estado do jogo online
        self.jogador_local = None    # 'X' para host, 'O' para cliente
        self.minha_vez = False       # Controla alternância de turnos
        self.conexao_ativa = False   # Flag de conexão estabelecida
        
        # Widgets da interface de conexão
        self.protocolo_var = None
        self.modo_conexao_var = None
        self.ip_entry = None
        self.porta_entry = None
        self.status_conexao = None
        
        # Widgets do jogo
        self.label_jogador = None
        
        # === INICIALIZAÇÃO ===
        self.mostrar_menu_principal()
        
    # =====================================================================
    # MÉTODOS DE NAVEGAÇÃO E LIMPEZA DA INTERFACE
    # =====================================================================
    
    def limpar_tela(self):
        """
        Remove todos os widgets da janela principal.
        
        Usado para transição entre diferentes telas (menus, jogo).
        Garante interface limpa antes de criar novos elementos.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # =====================================================================
    # MENUS DA INTERFACE GRÁFICA
    # =====================================================================
    
    def mostrar_menu_principal(self):
        """
        Exibe menu principal com 3 opções: Offline, Online, Sair.
        
        Layout:
        - Título centralizado
        - 3 botões verticalmente alinhados
        - Cores diferenciadas para cada opção
        - Botão sair com cor de alerta
        """
        self.limpar_tela()
        
        # === TÍTULO DO MENU ===
        titulo = tk.Label(self.root, text="JOGO DA VELHA", 
                         font=("Arial", 24, "bold"), fg="blue")
        titulo.pack(pady=30)
        
        # === BOTÕES DE NAVEGAÇÃO ===
        # Botão Modo 1v1 Local - cor verde suave
        btn_pvp = tk.Button(self.root, text="Jogo 1v1 Local", 
                           font=("Arial", 16), width=20, height=2,
                           command=lambda: self.iniciar_jogo("pvp"),
                           bg="lightgreen", activebackground="green")
        btn_pvp.pack(pady=10)
        
        # Botão Modo Online - cor azul suave
        btn_online = tk.Button(self.root, text="Jogo 1v1 Online", 
                              font=("Arial", 16), width=20, height=2,
                              command=self.mostrar_menu_online,
                              bg="lightblue", activebackground="blue")
        btn_online.pack(pady=10)
        
        # Botão Sair - cor vermelha suave (alerta)
        btn_sair = tk.Button(self.root, text="Sair", 
                            font=("Arial", 16), width=20, height=2,
                            command=self.sair_jogo,
                            bg="lightcoral", activebackground="red")
        btn_sair.pack(pady=10)
    
    def mostrar_menu_online(self):
        """
        Exibe interface de configuração para modo online.
        
        Elementos da interface:
        1. Seleção de protocolo (TCP/UDP) - Radio buttons
        2. Campo de entrada para IP
        3. Campo de entrada para porta
        4. Seleção de modo (Host/Cliente) - Radio buttons
        5. Botão conectar
        6. Label de status da conexão
        7. Botão voltar
        
        Layout organizado em grid para melhor alinhamento.
        """
        self.limpar_tela()
        
        # === TÍTULO ===
        titulo = tk.Label(self.root, text="JOGO 1v1 ONLINE", 
                         font=("Arial", 20, "bold"), fg="blue")
        titulo.pack(pady=15)
        
        # === FRAME PARA ORGANIZAÇÃO DOS CAMPOS ===
        # Usa grid layout para alinhamento preciso
        frame_config = tk.Frame(self.root)
        frame_config.pack(pady=10)
        
        # === 1. SELEÇÃO DE PROTOCOLO ===
        tk.Label(frame_config, text="Protocolo:", 
                font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        
        # Variável para armazenar seleção de protocolo
        self.protocolo_var = tk.StringVar(value="TCP")
        frame_protocolo = tk.Frame(frame_config)
        frame_protocolo.grid(row=0, column=1, sticky="w", padx=10)
        
        # Radio buttons para TCP e UDP
        tk.Radiobutton(frame_protocolo, text="TCP", variable=self.protocolo_var, 
                      value="TCP", font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Radiobutton(frame_protocolo, text="UDP", variable=self.protocolo_var, 
                      value="UDP", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        # === 2. CAMPO DE IP ===
        tk.Label(frame_config, text="IP:", 
                font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.ip_entry = tk.Entry(frame_config, font=("Arial", 11), width=20)
        self.ip_entry.grid(row=1, column=1, sticky="w", padx=10)
        # Valor padrão - localhost para testes
        self.ip_entry.insert(0, "127.0.0.1")
        
        # === 3. CAMPO DE PORTA ===
        tk.Label(frame_config, text="Porta:", 
                font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.porta_entry = tk.Entry(frame_config, font=("Arial", 11), width=20)
        self.porta_entry.grid(row=2, column=1, sticky="w", padx=10)
        # Porta padrão conforme seu projeto
        self.porta_entry.insert(0, "5555")
        
        # === 4. SELEÇÃO HOST/CLIENTE ===
        tk.Label(frame_config, text="Modo:", 
                font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        
        # Variável para armazenar seleção de modo
        self.modo_conexao_var = tk.StringVar(value="Host")
        frame_modo = tk.Frame(frame_config)
        frame_modo.grid(row=3, column=1, sticky="w", padx=10)
        
        # Radio buttons para Host e Cliente
        tk.Radiobutton(frame_modo, text="Host (Servidor)", variable=self.modo_conexao_var, 
                      value="Host", font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Radiobutton(frame_modo, text="Cliente", variable=self.modo_conexao_var, 
                      value="Cliente", font=("Arial", 10), padx=10).pack(side=tk.LEFT)
        
        # === INSTRUÇÕES PARA O USUÁRIO ===
        instrucoes = tk.Label(self.root, text="HOST: Use 0.0.0.0 para aceitar qualquer IP\nCLIENTE: Use o IP do host", 
                             font=("Arial", 9), fg="gray")
        instrucoes.pack(pady=5)
        
        # === 5. BOTÃO CONECTAR ===
        btn_conectar = tk.Button(self.root, text="Conectar", 
                                font=("Arial", 14), width=20, height=2,
                                command=self.iniciar_conexao_online,
                                bg="lightgreen", activebackground="green")
        btn_conectar.pack(pady=15)
        
        # === 6. LABEL DE STATUS ===
        # Mostra progresso da conexão e mensagens de erro
        self.status_conexao = tk.Label(self.root, text="", 
                                      font=("Arial", 11), fg="blue")
        self.status_conexao.pack(pady=5)
        
        # === 7. NAVEGAÇÃO ===
        btn_voltar = tk.Button(self.root, text="← Voltar", 
                              font=("Arial", 12), width=15,
                              command=self.mostrar_menu_principal,
                              bg="lightgray", activebackground="gray")
        btn_voltar.pack(pady=20)
    
    # =====================================================================
    # MÉTODOS DE PROTOCOLO DE APLICAÇÃO (BASEADOS NO SEU CÓDIGO ORIGINAL)
    # =====================================================================
    
    def criar_msg_jogada(self, linha, coluna):
        """
        Cria mensagem padronizada para transmitir jogada.
        Mantém compatibilidade com protocolo original.
        """
        return f"JOGADA|{linha}|{coluna}"

    def criar_msg_fim(self, vencedor):
        """
        Cria mensagem para indicar fim de jogo.
        Mantém compatibilidade com protocolo original.
        """
        return f"FIM_DE_JOGO|{vencedor}"

    def criar_msg_empate(self):
        """
        Cria mensagem para indicar empate.
        Mantém compatibilidade com protocolo original.
        """
        return "EMPATE"

    def interpretar_msg(self, msg):
        """
        Interpreta mensagem recebida do oponente.
        Código idêntico ao original para manter compatibilidade.
        """
        partes = msg.strip().split('|')
        tipo = partes[0]

        if tipo == "JOGADA":
            linha = int(partes[1])
            coluna = int(partes[2])
            return tipo, linha, coluna
        elif tipo == "FIM_DE_JOGO":
            return tipo, partes[1]
        elif tipo == "EMPATE":
            return tipo,
        else:
            return "ERRO",
    
    # =====================================================================
    # MÉTODOS DE CONEXÃO DE REDE
    # =====================================================================
    
    def iniciar_conexao_online(self):
        """
        Inicia processo de conexão de rede em thread separada.
        
        Validações:
        - Campos IP e porta preenchidos
        - Porta em range válido (1-65535)
        
        Fluxo:
        1. Valida entradas do usuário
        2. Atualiza status na interface
        3. Inicia thread de conexão (evita travamento da GUI)
        4. Thread chama estabelecer_conexao()
        """
        # === COLETA E VALIDAÇÃO DE DADOS ===
        ip = self.ip_entry.get().strip()
        porta = self.porta_entry.get().strip()
        protocolo = self.protocolo_var.get()
        modo = self.modo_conexao_var.get()
        
        # Validação básica de campos
        if not ip or not porta:
            messagebox.showerror("Erro", "Por favor, preencha IP e Porta!")
            return
            
        # Validação de porta numérica
        try:
            porta_num = int(porta)
            if porta_num < 1 or porta_num > 65535:
                raise ValueError("Porta inválida")
        except ValueError:
            messagebox.showerror("Erro", "Porta deve ser um número entre 1 e 65535!")
            return
        
        # === ATUALIZAÇÃO DE STATUS ===
        # Mostra mensagem apropriada baseada no modo
        if modo == "Host":
            self.status_conexao.config(
                text=f"Aguardando conexão... ({protocolo} - {ip}:{porta})", 
                fg="orange"
            )
        else:
            self.status_conexao.config(
                text=f"Conectando ao servidor... ({protocolo} - {ip}:{porta})", 
                fg="orange"
            )
        
        # Atualiza interface antes de iniciar thread
        self.root.update()
        
        # === THREAD DE CONEXÃO ===
        # Usa thread separada para evitar congelamento da GUI
        thread_conexao = threading.Thread(
            target=self.estabelecer_conexao,
            args=(protocolo, ip, porta_num, modo),
            daemon=True  # Thread finaliza com programa principal
        )
        thread_conexao.start()
    
    def estabelecer_conexao(self, protocolo, ip, porta, modo):
        """
        Estabelece conexão de rede usando lógica original do projeto.
        
        Executa em thread separada para não bloquear interface.
        Usa métodos originais do módulo p2p.
        
        Args:
            protocolo: 'TCP' ou 'UDP'
            ip: Endereço IP para conexão
            porta: Porta para conexão
            modo: 'Host' ou 'Cliente'
        
        Fluxo:
        1. Tenta estabelecer conexão usando funções originais
        2. Em caso de sucesso, configura variáveis de jogo
        3. Em caso de erro, mostra mensagem
        4. Usa self.root.after() para atualizar GUI thread-safe
        """
        try:
            # === ESTABELECIMENTO DE CONEXÃO ===
            if modo == "Host":
                # Modo host: aguarda conexão (função original)
                resultado = aguardar_conexao(protocolo, ip, porta)
                if resultado and len(resultado) == 2:
                    self.sock, self.endereco_remoto = resultado
                else:
                    self.sock = None
            else:
                # Modo cliente: conecta ao host (função original)
                resultado = conectar_cliente(protocolo, ip, porta)
                if resultado and len(resultado) == 2:
                    self.sock, self.endereco_remoto = resultado
                else:
                    self.sock = None
            
            # === TRATAMENTO DO RESULTADO ===
            if self.sock is None:
                # Falha na conexão
                self.root.after(0, self.callback_conexao_falhou)
            else:
                # Sucesso na conexão
                self.conexao_ativa = True
                # Host é sempre X, Cliente é sempre O (conforme original)
                self.jogador_local = 'X' if modo == "Host" else 'O'
                self.minha_vez = modo == "Host"  # Host começa jogando
                
                # Callback thread-safe para atualizar GUI
                self.root.after(0, self.callback_conexao_estabelecida)
                
        except Exception as e:
            # Erro durante conexão
            self.root.after(0, lambda: self.callback_erro_conexao(str(e)))
    
    def callback_conexao_estabelecida(self):
        """
        Callback executado na thread principal quando conexão é estabelecida.
        
        Thread-safe: chamado via self.root.after() da thread de rede.
        Atualiza interface e inicia jogo online.
        """
        self.status_conexao.config(text="Conexão estabelecida! Iniciando jogo...", fg="green")
        self.root.after(1500, lambda: self.iniciar_jogo("online"))
    
    def callback_conexao_falhou(self):
        """
        Callback executado quando conexão falha.
        Thread-safe: mostra erro na interface.
        """
        self.status_conexao.config(text="Falha ao estabelecer conexão!", fg="red")
    
    def callback_erro_conexao(self, erro):
        """
        Callback para erros durante processo de conexão.
        
        Args:
            erro: String com descrição do erro
        """
        self.status_conexao.config(text=f"Erro: {erro}", fg="red")
    
    # =====================================================================
    # MÉTODOS DE INICIALIZAÇÃO E CONTROLE DE JOGO
    # =====================================================================
    
    def iniciar_jogo(self, modo):
        """
        Inicializa novo jogo com modo especificado.
        
        Args:
            modo: 'pvp' ou 'online'
        
        Ações:
        1. Define modo de jogo
        2. Reseta estado do tabuleiro
        3. Cria interface de jogo
        4. Para modo online, inicia thread de recepção
        """
        self.modo_jogo = modo
        self.resetar_jogo()
        self.criar_interface_jogo()
        
        # === CONFIGURAÇÃO ESPECÍFICA PARA MODO ONLINE ===
        if modo == "online" and self.conexao_ativa:
            # Inicia thread para receber mensagens do oponente
            thread_recepcao = threading.Thread(
                target=self.thread_recepcao_online,
                daemon=True
            )
            thread_recepcao.start()
    
    def criar_interface_jogo(self):
        """
        Cria interface gráfica do jogo da velha.
        
        Layout:
        1. Título com informação do modo
        2. Label indicando jogador atual
        3. Grade 3x3 de botões (tabuleiro)
        4. Botões de controle (reiniciar, voltar)
        
        Para modo online:
        - Mostra símbolo do jogador local
        - Indica quando é sua vez ou do oponente
        """
        self.limpar_tela()
        
        # === 1. TÍTULO COM MODO DE JOGO ===
        if self.modo_jogo == "pvp":
            titulo_texto = "Jogo 1v1 Local"
        elif self.modo_jogo == "online":
            titulo_texto = f"Jogo 1v1 Online - Você é '{self.jogador_local}'"
        else:
            titulo_texto = "Jogo da Velha"
            
        titulo = tk.Label(self.root, text=titulo_texto, 
                         font=("Arial", 16, "bold"))
        titulo.pack(pady=10)
        
        # === 2. INDICADOR DE JOGADOR ATUAL ===
        if self.modo_jogo == "online":
            # Para modo online, mostra se é sua vez ou do oponente
            texto_jogador = "Sua vez!" if self.minha_vez else "Vez do oponente..."
        else:
            # Para modo offline, mostra jogador atual
            texto_jogador = f"Vez do jogador: {self.jogador_atual}"
            
        self.label_jogador = tk.Label(self.root, text=texto_jogador, 
                                     font=("Arial", 14))
        self.label_jogador.pack(pady=5)
        
        # === 3. TABULEIRO (GRADE 3x3) ===
        # Frame para conter o tabuleiro
        frame_tabuleiro = tk.Frame(self.root)
        frame_tabuleiro.pack(pady=20)
        
        # Criação dos botões em grade 3x3
        self.botoes_tabuleiro = []
        for i in range(3):
            linha_botoes = []
            for j in range(3):
                btn = tk.Button(
                    frame_tabuleiro, 
                    text="", 
                    font=("Arial", 20, "bold"), 
                    width=4, height=2,
                    command=lambda r=i, c=j: self.processar_jogada_gui(r, c),
                    bg="white",
                    relief="raised",
                    borderwidth=2
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                linha_botoes.append(btn)
            self.botoes_tabuleiro.append(linha_botoes)
        
        # === 4. CONTROLES DO JOGO ===
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=20)
        
        # Botão reiniciar
        btn_reiniciar = tk.Button(frame_controles, text="Reiniciar", 
                                 font=("Arial", 12), width=12,
                                 command=self.reiniciar_jogo,
                                 bg="lightgreen", activebackground="green")
        btn_reiniciar.pack(side=tk.LEFT, padx=5)
        
        # Botão voltar (dinâmico baseado no modo)
        btn_voltar = tk.Button(frame_controles, text="← Voltar", 
                              font=("Arial", 12), width=12,
                              command=self.voltar_menu_anterior,
                              bg="lightgray", activebackground="gray")
        btn_voltar.pack(side=tk.LEFT, padx=5)
    
    # =====================================================================
    # MÉTODOS DE JOGADA E LÓGICA DO JOGO
    # =====================================================================
    
    def processar_jogada_gui(self, linha, coluna):
        """
        Processa jogada clicada na interface gráfica.
        
        Comportamento varia conforme modo de jogo:
        - PvP: Alterna entre jogadores localmente
        - Online: Apenas se for sua vez, envia jogada para oponente
        
        Args:
            linha, coluna: Coordenadas da jogada (0-2)
        """
        # === VALIDAÇÃO PARA MODO ONLINE ===
        if self.modo_jogo == "online":
            if not self.minha_vez:
                # Não é sua vez - ignora clique
                return
            if not self.conexao_ativa:
                messagebox.showerror("Erro", "Conexão perdida!")
                return
        
        # === EXECUÇÃO DA JOGADA ===
        # Usa função original do módulo jogo
        if realizar_jogada(self.tabuleiro, linha, coluna, self.jogador_atual):
            # Jogada válida - atualiza interface
            self.atualizar_botao_tabuleiro(linha, coluna, self.jogador_atual)
            
            # === VERIFICAÇÃO DE FIM DE JOGO ===
            if verificar_vitoria(self.tabuleiro, self.jogador_atual):
                self.processar_vitoria(self.jogador_atual)
                return
                
            if verificar_empate(self.tabuleiro):
                self.processar_empate()
                return
            
            # === CONTINUAÇÃO DO JOGO ===
            if self.modo_jogo == "online":
                self.processar_jogada_online(linha, coluna)
            else:
                self.processar_jogada_offline()
    
    def processar_jogada_online(self, linha, coluna):
        """
        Processa jogada no modo online.
        
        Ações:
        1. Envia jogada para oponente
        2. Atualiza interface (não é mais sua vez)
        3. Em caso de vitória/empate, envia mensagem de fim
        
        Args:
            linha, coluna: Coordenadas da jogada realizada
        """
        # === ENVIO DA JOGADA ===
        mensagem = self.criar_msg_jogada(linha, coluna)
        if not enviar(self.sock, mensagem, self.protocolo_var.get(), self.endereco_remoto):
            messagebox.showerror("Erro", "Falha ao enviar jogada!")
            return
        
        # === ATUALIZAÇÃO DE TURNO ===
        self.minha_vez = False
        self.label_jogador.config(text="Vez do oponente...")
        
        # Nota: Verificação de fim de jogo já foi feita em processar_jogada_gui
    
    def processar_jogada_offline(self):
        """
        Processa continuação do jogo no modo offline (PvP).
        
        Alterna para próximo jogador.
        """
        # === ALTERNÂNCIA DE JOGADOR ===
        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
        
        # PvP: Apenas atualiza indicador
        self.label_jogador.config(text=f"Vez do jogador: {self.jogador_atual}")
    
    # =====================================================================
    # THREAD DE RECEPÇÃO PARA MODO ONLINE
    # =====================================================================
    
    def thread_recepcao_online(self):
        """
        Thread dedicada para receber mensagens do oponente.
        
        Executa loop contínuo recebendo mensagens via socket.
        Usa callbacks thread-safe para atualizar GUI.
        
        Loop:
        1. Recebe mensagem do oponente
        2. Interpreta tipo de mensagem
        3. Chama callback apropriado via self.root.after()
        4. Continua até conexão ser encerrada
        
        Tipos de mensagem tratados:
        - JOGADA: Oponente fez jogada
        - FIM_DE_JOGO: Oponente venceu
        - EMPATE: Jogo terminou em empate
        """
        while self.conexao_ativa:
            try:
                # === RECEPÇÃO DE MENSAGEM ===
                # Usa função original do módulo p2p
                msg, addr = receber(self.sock, self.protocolo_var.get())
                
                if msg is None:
                    # Erro na comunicação ou timeout
                    if self.conexao_ativa:  # Evita callback se conexão já encerrada
                        self.root.after(0, self.callback_erro_comunicacao)
                    break
                
                # === ATUALIZAÇÃO DE ENDEREÇO (UDP) ===
                # Para UDP, armazena endereço do remetente
                if self.protocolo_var.get() == 'UDP' and self.endereco_remoto is None:
                    self.endereco_remoto = addr
                
                # === INTERPRETAÇÃO DA MENSAGEM ===
                dados = self.interpretar_msg(msg)
                tipo = dados[0]
                
                # === CALLBACKS THREAD-SAFE ===
                if tipo == "JOGADA":
                    # Oponente fez jogada
                    _, linha, coluna = dados
                    self.root.after(0, lambda l=linha, c=coluna: self.callback_jogada_recebida(l, c))
                    
                elif tipo == "FIM_DE_JOGO":
                    # Oponente venceu
                    vencedor = dados[1]
                    self.root.after(0, lambda v=vencedor: self.callback_fim_jogo_recebido(v))
                    break
                    
                elif tipo == "EMPATE":
                    # Empate declarado pelo oponente
                    self.root.after(0, self.callback_empate_recebido)
                    break
                    
                else:
                    # Mensagem não reconhecida
                    self.root.after(0, lambda m=msg: self.callback_mensagem_desconhecida(m))
                    
            except Exception as e:
                # Erro na thread de recepção
                if self.conexao_ativa:
                    self.root.after(0, lambda erro=str(e): self.callback_erro_thread(erro))
                break
    
    # =====================================================================
    # CALLBACKS THREAD-SAFE PARA MODO ONLINE
    # =====================================================================
    
    def callback_jogada_recebida(self, linha, coluna):
        """
        Callback executado quando jogada do oponente é recebida.
        
        Thread-safe: chamado via self.root.after().
        
        Args:
            linha, coluna: Coordenadas da jogada do oponente
        
        Ações:
        1. Valida jogada recebida
        2. Atualiza tabuleiro e interface
        3. Verifica condições de fim de jogo
        4. Passa turno para jogador local
        """
        # === DETERMINAÇÃO DO SÍMBOLO DO OPONENTE ===
        jogador_remoto = 'O' if self.jogador_local == 'X' else 'X'
        
        # === EXECUÇÃO DA JOGADA DO OPONENTE ===
        if realizar_jogada(self.tabuleiro, linha, coluna, jogador_remoto):
            # Jogada válida - atualiza interface
            self.atualizar_botao_tabuleiro(linha, coluna, jogador_remoto)
            
            # === VERIFICAÇÃO DE FIM DE JOGO ===
            # Nota: Oponente já verificou e enviará mensagem de fim se necessário
            # Aqui apenas passamos o turno de volta
            
            # === RETORNO DO TURNO ===
            self.minha_vez = True
            self.jogador_atual = self.jogador_local
            self.label_jogador.config(text="Sua vez!")
            
        else:
            # Jogada inválida recebida (erro de protocolo)
            messagebox.showerror("Erro", "Jogada inválida recebida do oponente!")
    
    def callback_fim_jogo_recebido(self, vencedor):
        """
        Callback para mensagem de fim de jogo recebida.
        
        Args:
            vencedor: Símbolo do jogador vencedor
        """
        self.conexao_ativa = False
        if vencedor == self.jogador_local:
            messagebox.showinfo("Fim de Jogo", "Você venceu!")
        else:
            messagebox.showinfo("Fim de Jogo", "Você perdeu!")
        
        # Desabilita tabuleiro
        self.desabilitar_tabuleiro()
    
    def callback_empate_recebido(self):
        """
        Callback para mensagem de empate recebida.
        """
        self.conexao_ativa = False
        messagebox.showinfo("Fim de Jogo", "Empate!")
        self.desabilitar_tabuleiro()
    
    def callback_erro_comunicacao(self):
        """
        Callback para erro de comunicação.
        """
        self.conexao_ativa = False
        messagebox.showerror("Erro", "Erro na comunicação com oponente!")
    
    def callback_mensagem_desconhecida(self, msg):
        """
        Callback para mensagem não reconhecida.
        
        Args:
            msg: Mensagem recebida não reconhecida
        """
        print(f"Mensagem desconhecida recebida: {msg}")
    
    def callback_erro_thread(self, erro):
        """
        Callback para erro na thread de recepção.
        
        Args:
            erro: Descrição do erro
        """
        self.conexao_ativa = False
        messagebox.showerror("Erro", f"Erro na thread de recepção: {erro}")
    
    # =====================================================================
    # MÉTODOS DE ATUALIZAÇÃO DA INTERFACE
    # =====================================================================
    
    def atualizar_botao_tabuleiro(self, linha, coluna, jogador):
        """
        Atualiza botão específico do tabuleiro com símbolo do jogador.
        
        Args:
            linha, coluna: Posição no tabuleiro (0-2)
            jogador: Símbolo do jogador ('X' ou 'O')
        
        Aplica cores diferentes:
        - X: Vermelho
        - O: Azul
        """
        self.botoes_tabuleiro[linha][coluna].config(
            text=jogador,
            fg="red" if jogador == "X" else "blue",
            state="disabled"  # Previne cliques duplos
        )
    
    def desabilitar_tabuleiro(self):
        """
        Desabilita todos os botões do tabuleiro.
        
        Usado quando jogo termina para prevenir jogadas adicionais.
        """
        for linha in self.botoes_tabuleiro:
            for btn in linha:
                btn.config(state="disabled")
    
    # =====================================================================
    # MÉTODOS DE PROCESSAMENTO DE FIM DE JOGO
    # =====================================================================
    
    def processar_vitoria(self, vencedor):
        """
        Processa vitória no jogo.
        
        Args:
            vencedor: Símbolo do jogador vencedor
        
        Comportamento varia por modo:
        - Offline: Mostra popup simples
        - Online: Envia mensagem para oponente e mostra resultado
        """
        if self.modo_jogo == "online" and self.conexao_ativa:
            # === MODO ONLINE ===
            # Envia mensagem de fim para oponente
            enviar(self.sock, self.criar_msg_fim(vencedor), 
                  self.protocolo_var.get(), self.endereco_remoto)
            self.conexao_ativa = False
            
            # Determina mensagem baseada em quem venceu
            if vencedor == self.jogador_local:
                messagebox.showinfo("Fim de Jogo", "Você venceu!")
            else:
                messagebox.showinfo("Fim de Jogo", "Você perdeu!")
        else:
            # === MODO OFFLINE ===
            messagebox.showinfo("Fim de Jogo", f"Jogador {vencedor} venceu!")
        
        # Desabilita tabuleiro
        self.desabilitar_tabuleiro()
    
    def processar_empate(self):
        """
        Processa empate no jogo.
        
        Para modo online, notifica oponente.
        Para modo offline, apenas mostra resultado.
        """
        if self.modo_jogo == "online" and self.conexao_ativa:
            # === MODO ONLINE ===
            # Envia mensagem de empate para oponente
            enviar(self.sock, self.criar_msg_empate(), 
                  self.protocolo_var.get(), self.endereco_remoto)
            self.conexao_ativa = False
        
        # === EXIBIÇÃO DO RESULTADO ===
        messagebox.showinfo("Fim de Jogo", "Empate!")
        self.desabilitar_tabuleiro()
    
    # =====================================================================
    # MÉTODOS DE CONTROLE DE ESTADO DO JOGO
    # =====================================================================
    
    def resetar_jogo(self):
        """
        Reseta estado do jogo para nova partida.
        
        Ações:
        - Limpa tabuleiro
        - Reseta jogador atual para 'X'
        - Mantém configurações de rede (modo online)
        """
        # Usa função original para criar tabuleiro limpo
        self.tabuleiro = criar_tabuleiro()
        self.jogador_atual = "X"
        
        # Para modo online, reseta estado de turno
        if self.modo_jogo == "online":
            # Host (X) sempre começa
            self.minha_vez = (self.jogador_local == 'X')
    
    def reiniciar_jogo(self):
        """
        Reinicia jogo atual mantendo mesmo modo.
        
        Para modo online:
        - Apenas reseta tabuleiro local (não coordena com oponente)
        - Funcionalidade limitada - idealmente requereria protocolo de reinício
        """
        if self.modo_jogo == "online":
            # Aviso sobre limitação no modo online
            resposta = messagebox.askyesno(
                "Reiniciar Jogo Online",
                "Reiniciar em modo online apenas limpa seu tabuleiro.\n"
                "O oponente não será notificado.\n"
                "Deseja continuar?"
            )
            if not resposta:
                return
        
        # Reseta e recria interface
        self.resetar_jogo()
        self.criar_interface_jogo()
    
    def voltar_menu_anterior(self):
        """
        Volta para menu anterior baseado no modo atual.
        
        Para modo online, encerra conexão antes de voltar.
        """
        # === LIMPEZA PARA MODO ONLINE ===
        if self.modo_jogo == "online":
            # Encerra conexão de forma segura
            self.conexao_ativa = False
            if self.sock:
                try:
                    encerrar(self.sock)  # Usa função original
                except:
                    pass  # Ignora erros de encerramento
                self.sock = None
        
        # === NAVEGAÇÃO ===
        if self.modo_jogo == "online":
            self.mostrar_menu_online()
        else:
            self.mostrar_menu_principal()
    
    def sair_jogo(self):
        """
        Encerra aplicação de forma segura.
        
        Garante que conexões de rede sejam fechadas antes de sair.
        """
        # === LIMPEZA DE RECURSOS ===
        if self.modo_jogo == "online" and self.sock:
            try:
                self.conexao_ativa = False
                encerrar(self.sock)  # Usa função original
            except:
                pass  # Ignora erros durante encerramento
        
        # === ENCERRAMENTO DA APLICAÇÃO ===
        self.root.quit()
        self.root.destroy()
    
    def executar(self):
        """
        Inicia loop principal da interface gráfica.
        
        Método público para iniciar aplicação.
        Configura tratamento de fechamento da janela.
        """
        # === CONFIGURAÇÃO DE ENCERRAMENTO ===
        # Garante limpeza quando janela é fechada
        self.root.protocol("WM_DELETE_WINDOW", self.sair_jogo)
        
        # === LOOP PRINCIPAL ===
        self.root.mainloop()


# =====================================================================
# PONTO DE ENTRADA DA APLICAÇÃO
# =====================================================================

def main():
    """
    Função principal - ponto de entrada da aplicação.
    
    Cria instância da classe principal e inicia interface gráfica.
    Substitui a função main() original que usava interface de linha de comando.
    """
    try:
        # Cria e executa aplicação GUI
        app = JogoDaVelhaGUI()
        app.executar()
    except Exception as e:
        # Tratamento de erro geral
        print(f"Erro na aplicação: {e}")
        import traceback
        traceback.print_exc()

# === EXECUÇÃO PRINCIPAL ===
if __name__ == '__main__':
    """
    Ponto de entrada padrão do Python.
    
    Executa apenas quando arquivo é executado diretamente.
    Mantém compatibilidade com estrutura original.
    """
    main()