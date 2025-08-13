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


