# ZeroMQ - Execução em Máquinas Distribuídas

Este repositório contém três padrões de comunicação ZeroMQ modificados para execução em máquinas diferentes:

1. **Cliente-Servidor** (Request-Reply)
2. **Publisher-Subscriber**
3. **Producer-Worker** (Pipeline)

## 📋 Pré-requisitos

Em todas as máquinas, instale as dependências:

```bash
pip install pyzmq
```

## 🔧 Configuração de Firewall

Para que a comunicação funcione entre máquinas diferentes, certifique-se de que as portas estejam abertas no firewall:

### Linux (Ubuntu/Debian):
```bash
sudo ufw allow 12345/tcp
sudo ufw allow 5678/tcp
sudo ufw allow 5679/tcp
```

### Windows:
```powershell
New-NetFirewallRule -DisplayName "ZeroMQ" -Direction Inbound -Protocol TCP -LocalPort 12345,5678,5679 -Action Allow
```

## 🌐 Descobrindo o IP da Máquina

### Linux/Mac:
```bash
hostname -I
# ou
ip addr show
```

### Windows:
```powershell
ipconfig
```

---

## 1️⃣ Cliente-Servidor (Request-Reply)

Neste padrão, o cliente envia requisições e o servidor responde.

### Execução Local (teste):

**Terminal 1 - Servidor:**
```bash
cd client-server
python server.py
```

**Terminal 2 - Cliente:**
```bash
cd client-server
python client.py localhost
```

### Execução em Máquinas Diferentes:

**Máquina A (Servidor) - IP: 192.168.1.100**
```bash
cd client-server
python server.py 12345
# O servidor mostrará: "Clients should connect to: tcp://192.168.1.100:12345"
```

**Máquina B (Cliente)**
```bash
cd client-server
python client.py 192.168.1.100 12345
# ou com mensagem customizada:
python client.py 192.168.1.100 12345 "Olá do cliente!"
```

### Testando com múltiplos clientes:

Você pode executar vários clientes simultaneamente conectando à mesma porta do servidor (mas em terminais diferentes, já que é request-reply e funciona sequencialmente).

---

## 2️⃣ Publisher-Subscriber

Neste padrão, o publisher envia mensagens que múltiplos subscribers podem receber.

### Execução Local (teste):

**Terminal 1 - Publisher:**
```bash
cd pub-sub
python publisher.py
```

**Terminal 2 - Subscriber:**
```bash
cd pub-sub
python subscriber.py localhost
```

### Execução em Máquinas Diferentes:

**Máquina A (Publisher) - IP: 192.168.1.100**
```bash
cd pub-sub
python publisher.py 12345 5
# Publica a cada 5 segundos
# Mostrará: "Subscribers should connect to: tcp://192.168.1.100:12345"
```

**Máquina B (Subscriber 1)**
```bash
cd pub-sub
python subscriber.py 192.168.1.100 12345 10
# Recebe 10 mensagens
```

**Máquina C (Subscriber 2)**
```bash
cd pub-sub
python subscriber.py 192.168.1.100 12345 5
# Recebe 5 mensagens
```

### Múltiplos Subscribers:

O padrão pub-sub permite que vários subscribers se conectem simultaneamente ao mesmo publisher. Cada subscriber receberá todas as mensagens publicadas (respeitando seus filtros).

---

## 3️⃣ Producer-Worker (Pipeline)

Neste padrão, o producer distribui tarefas para múltiplos workers que as processam em paralelo.

### Execução Local (teste):

**Terminal 1 - Producer:**
```bash
cd pipeline_producer-consumer
python producer.py 12345 20
# Pressione Enter para começar a distribuir tarefas
```

**Terminal 2 - Worker 1:**
```bash
cd pipeline_producer-consumer
python worker.py 1 localhost:12345
```

**Terminal 3 - Worker 2:**
```bash
cd pipeline_producer-consumer
python worker.py 2 localhost:12345
```

### Execução em Máquinas Diferentes:

**Máquina A (Producer) - IP: 192.168.1.100**
```bash
cd pipeline_producer-consumer
python producer.py 12345 100
# Distribui 100 tarefas
# Pressione Enter quando os workers estiverem prontos
```

**Máquina B (Worker 1)**
```bash
cd pipeline_producer-consumer
python worker.py W1 192.168.1.100:12345
```

**Máquina C (Worker 2)**
```bash
cd pipeline_producer-consumer
python worker.py W2 192.168.1.100:12345
```

**Máquina D (Worker 3)**
```bash
cd pipeline_producer-consumer
python worker.py W3 192.168.1.100:12345
```

### Conectando a Múltiplos Producers:

Um worker pode se conectar a múltiplos producers simultaneamente:

```bash
python worker.py W1 192.168.1.100:12345 192.168.1.101:5678
```

---

## 🔍 Verificação e Troubleshooting

### Testando conectividade:

**Verificar se a porta está aberta:**
```bash
# Na máquina servidor
netstat -tuln | grep 12345

# De outra máquina
telnet 192.168.1.100 12345
# ou
nc -zv 192.168.1.100 12345
```

### Problemas comuns:

1. **"Connection refused"**
   - Verifique se o servidor está rodando
   - Confirme que o firewall permite a porta
   - Verifique se o IP está correto

2. **"No route to host"**
   - Verifique a conectividade de rede
   - Confirme que as máquinas estão na mesma rede (ou têm roteamento configurado)

3. **Mensagens não chegam no pub-sub**
   - Aguarde alguns segundos após conectar o subscriber (ZeroMQ pode perder mensagens iniciais)
   - Verifique se o filtro está correto

4. **Workers não recebem tarefas uniformemente**
   - Isso é esperado! ZeroMQ distribui as tarefas conforme os workers ficam disponíveis
   - Workers mais rápidos receberão mais tarefas

---

## 📊 Exemplos de Cenários de Teste

### Cenário 1: Teste Básico Local
Use `localhost` em todos os comandos para validar que o código funciona.

### Cenário 2: Servidor em uma máquina, cliente em outra
- Máquina 1: `python server.py`
- Máquina 2: `python client.py <IP-máquina-1>`

### Cenário 3: Producer em uma máquina, múltiplos workers em outras
- Máquina 1: `python producer.py`
- Máquinas 2-5: `python worker.py <id> <IP-máquina-1>:12345`

### Cenário 4: Publisher em uma máquina, subscribers em várias outras
- Máquina 1: `python publisher.py`
- Máquinas 2-4: `python subscriber.py <IP-máquina-1>`

---

## 📝 Observações Importantes

1. **Binding vs Connecting:**
   - Servidores/Publishers/Producers fazem `bind()` em `tcp://*:porta`
   - Clientes/Subscribers/Workers fazem `connect()` em `tcp://IP:porta`

2. **Ordem de execução:**
   - Sempre inicie primeiro o componente que faz `bind()` (servidor, publisher, producer)
   - Depois conecte os componentes que fazem `connect()`

3. **Performance:**
   - A rede pode adicionar latência comparado à execução local
   - Use logs (`print`) para acompanhar o fluxo de mensagens

4. **Encerramento:**
   - Use Ctrl+C para encerrar os programas gracefully
   - Os workers mostrarão estatísticas ao encerrar

---

## 🎯 Estrutura dos Arquivos

```
zeromq-rafaeltaveira-cpu-main/
├── client-server/
│   ├── server.py          # Novo: servidor standalone
│   ├── client.py          # Novo: cliente standalone
│   └── zmq_client-server.py  # Original (local)
│
├── pub-sub/
│   ├── publisher.py       # Novo: publisher standalone
│   ├── subscriber.py      # Novo: subscriber standalone
│   └── zmq_pub-sub.py     # Original (local)
│
└── pipeline_producer-consumer/
    ├── producer.py        # Novo: producer standalone
    ├── worker.py          # Novo: worker standalone
    ├── tasksrc.py         # Versão intermediária
    ├── taskwork.py        # Versão intermediária
    ├── constPipe.py       # Constantes antigas
    └── zmq_producer-worker.py  # Original (local)
```

---

## ✅ Checklist para Entrega

- [ ] Código funciona localmente (teste com localhost)
- [ ] Código funciona entre máquinas diferentes
- [ ] Firewall configurado para permitir as portas
- [ ] README.md atualizado com instruções
- [ ] Screenshots ou logs demonstrando execução distribuída
- [ ] Repositório GitHub Classroom atualizado

---

## 🤝 Contribuindo

Este é um projeto acadêmico. Consulte o professor para dúvidas sobre os requisitos da tarefa.

## 📚 Referências

- [ZeroMQ Guide](https://zguide.zeromq.org/)
- Tanenbaum & van Steen (2025) - Distributed Systems
