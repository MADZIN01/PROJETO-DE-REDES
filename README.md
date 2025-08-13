# 🎮 Jogo da Velha Python - P2P Online

Um jogo da velha (tic-tac-toe) implementado em Python com interface gráfica Tkinter e funcionalidade multiplayer peer-to-peer.  
Suporta modo local (1v1 no mesmo computador) e modo online com comunicação TCP/UDP e IPv4/IPv6.

---

## ✨ Características

- 🎯 **Interface Gráfica:** Interface amigável com Tkinter  
- 🌐 **Modo Online P2P:** Comunicação direta entre jogadores sem servidor dedicado  
- 🔗 **Protocolos Múltiplos:** Suporte completo a TCP e UDP  
- 🌍 **IPv4 e IPv6:** Compatibilidade com ambas as versões do protocolo IP  
- 🏠 **Modo Local:** Jogo 1v1 no mesmo computador  
- 🚀 **Fácil Inicialização:** Script `.bat` incluído para Windows  

---
## 📋 Pré-requisitos

- Python 3.7 ou superior — [Download Python](https://www.python.org/downloads/)
- Tkinter (geralmente incluído com Python)
- Conexão com a internet (apenas para modo online)

---
## 🚀 Evolução do Projeto

### v0.1 — Estrutura inicial
- Lógica básica do jogo da velha, apenas modo local.
- Sem rede, sem modularização avançada.

---

### v0.2 — Introdução do modo online (TCP)
**feat:** implementação do sistema P2P básico com TCP
- Modulariza código em `jogo.py`, `p2p.py` e `main.py`.
- Adiciona comunicação TCP host/cliente.
- Cria scripts `.bat` para facilitar inicialização.
- Mantém compatibilidade da lógica original.

---

### v0.3 — Suporte ao protocolo UDP
**feat:** suporte UDP e unificação de interface de protocolos
- Implementa suporte dual TCP/UDP com seleção pelo usuário.
- Unifica API de comunicação para ambos protocolos.
- Melhora tratamento de endereçamento para UDP.
- Substitui scripts separados por `setup.bat` unificado.
- Adiciona validação e tratamento de erros de rede.

---

### v0.5 — Modularização sólida e melhorias
**feat:** sistema híbrido com refatoração completa
- Adiciona modo offline (`main_offline.py`).
- Refatora `jogo.py` para funções puras sem estado global.
- Implementa menu principal com seleção de modalidade.
- Adiciona função `verificar_empate()` para melhor UX.
- Melhora interface visual do tabuleiro.
- Cria `setup.bat` com loop de menu.

---

### v1.0 — Protocolo de aplicação completo
**feat:** lançamento com funcionalidades robustas
- Implementa protocolo de mensagens estruturado (`JOGADA|FIM_DE_JOGO|EMPATE`).
- Adiciona suporte completo IPv4/IPv6 com detecção automática.
- Interface profissional com tabuleiro gráfico e menu limpo.
- Implementa `realizar_jogada()` e `encerrar()` para melhor organização.
- Melhora tratamento de erros e validação de entrada.
- Muda sistema de coordenadas de 0-2 para 1-3.
- Substitui comunicação simples por protocolo estruturado.

---

### v2.0 — Interface gráfica completa (Tkinter)
**feat:** GUI moderna e intuitiva
- Substitui interface CLI por GUI visual com cores (X=vermelho, O=azul).
- Cria tabuleiro clicável e menus hierárquicos.
- Implementa comunicação thread-safe para manter GUI responsiva.
- Mantém 100% de compatibilidade com código original.
- Preserva protocolo TCP/UDP e IPv4/IPv6.

> Git tag: `git tag -a v2.0-gui -m "v2.0 - Interface gráfica completa"`

## 📥 Como baixar e instalar

**Método 1 — Clone com Git**
```bash
git clone [https://github.com/MADZIN01/PROJETO-DE-REDES..git]
cd jogo-da-velha-python
```

**Método 2 — Download ZIP**
1. Baixe o arquivo ZIP do repositório  
2. Extraia em uma pasta de sua escolha  
3. Navegue até a pasta no terminal:
```bash
cd caminho/para/jogo-da-velha-python
```

---

## ▶️ Como executar o jogo

**Windows (Recomendado)**
```bash
start.jogo.bat
```

**Linha de comando (qualquer sistema)**
```bash
python main.py
# ou
python3 main.py
```
---

## 🎮 Como jogar

### 🏠 Modo Local (1v1 Mesmo Computador)
1. Execute o jogo  
2. Clique em "Jogo 1v1 Local"  
3. Clique nas células da grade 3x3 para fazer jogadas  
4. Jogadores se alternam automaticamente (X começa primeiro)  
5. Vence quem conseguir 3 símbolos em linha, coluna ou diagonal  

### 🌐 Modo Online (1v1 Pela Internet/Rede)
**Configuração Básica**
1. Execute o jogo  
2. Clique em "Jogo 1v1 Online"  
3. Configure as opções:  
   - **Protocolo:** TCP (recomendado) ou UDP  
   - **IP:** Endereço de conexão  
   - **Porta:** Porta de comunicação (padrão: 5555)  
   - **Modo:** Host (servidor) ou Cliente  

**Jogando na mesma rede (LAN)**  
- **Host:**  
  - IP: `0.0.0.0`  
  - Anote seu IP local (ex: `192.168.1.100`)  
- **Cliente:**  
  - Digite o IP do Host  
  - Use a mesma porta  

**Jogando pela Internet**
- Configure port forwarding no roteador  
- Descubra seu IP público em [whatismyipaddress.com](https://whatismyipaddress.com)  
- Cliente conecta usando esse IP

---

## 📡 Protocolos Disponíveis

**TCP (Recomendado)**
- ✅ Confiável
- ✅ Ordenado
- ❌ Ligeiramente mais lento que UDP

**UDP**
- ✅ Mais rápido
- ❌ Não confiável

---

## 🎮 Controles da Interface

**Durante o Jogo**
- Clique do Mouse: Fazer jogada na célula  
- Botão Reiniciar: Nova partida  
- Botão Voltar: Retorna ao menu  

**Navegação**
- Menu Principal: Escolha entre Local, Online ou Sair  
- Menu Online: Configuração de rede e conexão  

---

## 🔍 Solução de Problemas

**❌ "Módulo tkinter não encontrado"**
```bash
# Linux
sudo apt-get install python3-tk
# ou
sudo yum install tkinter
```
Windows/Mac: reinstale Python com "Add to PATH" marcado  

**❌ "Erro ao fazer bind/listen"**
- Porta em uso: escolha outra (ex: 8080)  
- IP inválido  

**❌ "Timeout recebendo dados"**
- Verifique firewall  
- Confirme IP e porta corretos  

**❌ "Address already in use"**
- Aguarde 30-60 segundos ou use outra porta  

---

## 🔄 Fluxo de Conexão

**TCP**
1. Host → `bind()` e `listen()`  
2. Cliente → `connect()`  
3. Host → `accept()`  
4. Comunicação estabelecida  

**UDP**
1. Host → `bind()` e aguarda pacote  
2. Cliente → envia `"CONEXAO_UDP"`  
3. Host → responde `"CONEXAO_CONFIRMADA"`  

---

## ⚡ Iniciando Rapidamente

**Windows**
```bash
start.jogo.bat
```


**Primeira partida online**
- Host: IP `0.0.0.0`, Porta `5555`, TCP, Host  
- Cliente: IP do Host, Porta `5555`, TCP, Cliente  
💡 Para testes locais, use IP `127.0.0.1` nos dois jogadores.

---
🎯 **Divirta-se jogando este clássico jogo da velha com tecnologia moderna!**

## DESENVOLVEDORES : 
1. Madson Alessio 
2. Julio Santos 
3. Abraao Araujo
4. Eduado Torres 
5. Davi lucas nobrega 


