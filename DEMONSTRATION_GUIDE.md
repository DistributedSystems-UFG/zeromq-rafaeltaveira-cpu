# Guia de Demonstração - Execução Distribuída

Este documento ajuda você a documentar que os exemplos ZeroMQ estão funcionando em máquinas diferentes.

## 📸 O que Documentar

Para cada padrão (Cliente-Servidor, Pub-Sub, Producer-Worker), você deve demonstrar:

1. **Screenshots ou logs** mostrando:
   - Servidor/Publisher/Producer rodando em uma máquina (com IP visível)
   - Cliente/Subscriber/Worker rodando em outra máquina conectando ao IP correto
   - Mensagens sendo trocadas com sucesso

2. **Informações de contexto**:
   - IPs das máquinas envolvidas
   - Portas utilizadas
   - Saída dos comandos mostrando conexão bem-sucedida

## 🎯 Exemplo de Demonstração: Cliente-Servidor

### Cenário
- Máquina A (Servidor): IP 192.168.1.100
- Máquina B (Cliente): IP 192.168.1.101

### Passo 1: Verificar IP das Máquinas

**Máquina A:**
```bash
hostname -I
# Saída: 192.168.1.100
```

**Máquina B:**
```bash
hostname -I
# Saída: 192.168.1.101
```

### Passo 2: Executar Servidor na Máquina A

```bash
cd client-server
python server.py 12345
```

**Saída esperada:**
```
Starting server on port 12345...
[SERVER] Listening on tcp://*:12345
[SERVER] Clients should connect to: tcp://192.168.1.100:12345
```

📸 **TIRAR SCREENSHOT AQUI** mostrando:
- O comando executado
- IP da máquina (pode usar `hostname -I` em outro terminal)
- Mensagem de que o servidor está escutando

### Passo 3: Executar Cliente na Máquina B

```bash
cd client-server
python client.py 192.168.1.100 12345
```

**Saída esperada no Cliente:**
```
[CLIENT] Connecting to tcp://192.168.1.100:12345...
[CLIENT] Sending: Hello world
[CLIENT] Received: Hello world*
[CLIENT] Sending STOP command...
[CLIENT] Final response: Server shutting down
[CLIENT] Client finished.
```

**Saída esperada no Servidor (Máquina A):**
```
[SERVER] Received message #1: Hello world
[SERVER] Sent reply: Hello world*
[SERVER] Received STOP command. Shutting down...
[SERVER] Server stopped.
```

📸 **TIRAR SCREENSHOTS** mostrando:
- Terminal do Cliente na Máquina B com IP 192.168.1.101
- Terminal do Servidor na Máquina A com IP 192.168.1.100
- Mensagens sendo trocadas com sucesso

---

## 🎯 Exemplo de Demonstração: Pub-Sub

### Cenário
- Máquina A (Publisher): IP 192.168.1.100
- Máquina B (Subscriber 1): IP 192.168.1.101
- Máquina C (Subscriber 2): IP 192.168.1.102

### Comandos

**Máquina A:**
```bash
cd pub-sub
python publisher.py 12345 3
```

**Máquina B:**
```bash
cd pub-sub
python subscriber.py 192.168.1.100 12345 5
```

**Máquina C:**
```bash
cd pub-sub
python subscriber.py 192.168.1.100 12345 5
```

📸 **DOCUMENTAR**:
- Publisher publicando mensagens
- Ambos subscribers recebendo as mesmas mensagens
- IPs de cada máquina

---

## 🎯 Exemplo de Demonstração: Producer-Worker

### Cenário
- Máquina A (Producer): IP 192.168.1.100
- Máquina B (Worker 1): IP 192.168.1.101
- Máquina C (Worker 2): IP 192.168.1.102
- Máquina D (Worker 3): IP 192.168.1.103

### Comandos

**Máquina A:**
```bash
cd pipeline_producer-consumer
python producer.py 12345 50
# Aguarde os workers conectarem, depois pressione Enter
```

**Máquina B:**
```bash
cd pipeline_producer-consumer
python worker.py W1 192.168.1.100:12345
```

**Máquina C:**
```bash
cd pipeline_producer-consumer
python worker.py W2 192.168.1.100:12345
```

**Máquina D:**
```bash
cd pipeline_producer-consumer
python worker.py W3 192.168.1.100:12345
```

📸 **DOCUMENTAR**:
- Producer distribuindo tarefas
- Múltiplos workers processando em paralelo
- Estatísticas finais de cada worker
- IPs de todas as máquinas

---

## 📝 Template de Relatório

Use este template para documentar sua implementação:

```markdown
# Execução Distribuída - ZeroMQ

## 1. Cliente-Servidor

### Configuração
- Servidor: Máquina A (IP: ___)
- Cliente: Máquina B (IP: ___)
- Porta: 12345

### Screenshots
[Inserir screenshot do servidor]
[Inserir screenshot do cliente]

### Observações
- Conexão estabelecida com sucesso
- Mensagens trocadas corretamente
- Comando STOP funcionou

---

## 2. Publisher-Subscriber

### Configuração
- Publisher: Máquina A (IP: ___)
- Subscriber 1: Máquina B (IP: ___)
- Subscriber 2: Máquina C (IP: ___)
- Porta: 12345

### Screenshots
[Inserir screenshots]

### Observações
- Múltiplos subscribers receberam as mesmas mensagens
- Padrão pub-sub funcionou corretamente

---

## 3. Producer-Worker

### Configuração
- Producer: Máquina A (IP: ___)
- Worker 1: Máquina B (IP: ___)
- Worker 2: Máquina C (IP: ___)
- Worker 3: Máquina D (IP: ___)
- Porta: 12345

### Screenshots
[Inserir screenshots]

### Estatísticas
Worker 1: X tarefas processadas
Worker 2: Y tarefas processadas
Worker 3: Z tarefas processadas

### Observações
- Tarefas distribuídas entre os workers
- Balanceamento de carga funcionou
- Todos os workers processaram tarefas

---

## Conclusão

Todos os três padrões foram implementados com sucesso e testados em máquinas diferentes.
As modificações permitiram que os componentes executassem de forma distribuída,
mantendo a funcionalidade original dos exemplos.
```

---

## 🔍 Checklist de Verificação

Antes de fazer a entrega, verifique:

- [ ] Testou localmente primeiro (use `test_local.py`)
- [ ] Configurou firewall para permitir as portas
- [ ] Verificou IPs de todas as máquinas
- [ ] Executou cada padrão em máquinas diferentes
- [ ] Capturou screenshots/logs de cada execução
- [ ] Screenshots mostram IPs das máquinas
- [ ] Todos os três padrões funcionaram
- [ ] Producer-Worker tem pelo menos 2 workers em máquinas diferentes
- [ ] Criou relatório/documentação da execução
- [ ] Código commitado no GitHub Classroom

---

## 💡 Dicas para Screenshots

1. **Use terminais com títulos claros**: Configure o título do terminal para mostrar "Servidor - 192.168.1.100" ou similar

2. **Mostre múltiplas janelas**: Se possível, capture os dois lados da comunicação em uma única imagem

3. **Destaque informações importantes**: Circle ou arrow apontando para:
   - IPs nas mensagens
   - Mensagens sendo trocadas
   - Status de conexão

4. **Use ferramentas**:
   - Linux: `gnome-screenshot`, `scrot`, `flameshot`
   - Mac: Cmd+Shift+4
   - Windows: Snipping Tool, Win+Shift+S

5. **Grave um vídeo**: Se possível, grave um screencast mostrando toda a execução

---

## 🚀 Testes Sugeridos

### Teste Mínimo (para aprovação)
- Cliente-Servidor: 1 servidor + 1 cliente em máquinas diferentes
- Pub-Sub: 1 publisher + 1 subscriber em máquinas diferentes
- Producer-Worker: 1 producer + 2 workers em máquinas diferentes

### Teste Completo (para demonstração excelente)
- Cliente-Servidor: 1 servidor + múltiplos clientes sequenciais
- Pub-Sub: 1 publisher + 3+ subscribers simultâneos
- Producer-Worker: 1 producer + 5+ workers distribuídos em 3+ máquinas

### Teste Avançado (extras)
- Producer-Worker com 2 producers e workers conectando a ambos
- Pub-Sub com filtros diferentes em subscribers diferentes
- Medição de latência/throughput entre máquinas locais vs. remotas
