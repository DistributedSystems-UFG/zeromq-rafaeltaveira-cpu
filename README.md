[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wa7oHGos)

# ZeroMQ - Execução Distribuída em Máquinas Diferentes

Este repositório contém exemplos modificados de três padrões de comunicação ZeroMQ que podem ser executados em **máquinas diferentes**.

**Exemplos baseados em:** Tanenbaum & van Steen (2025) - Distributed Systems

## 🎯 Objetivo da Tarefa

Modificar os três exemplos originais (que executavam localmente) para permitir execução dos componentes em máquinas diferentes:

1. ✅ **Cliente-Servidor** (Request-Reply)
2. ✅ **Publisher-Subscriber**
3. ✅ **Producer-Worker** (Pipeline)

## 📁 Estrutura do Repositório

```
zeromq-rafaeltaveira-cpu-main/
│
├── 📖 README.md                    # Este arquivo
├── 📖 INSTRUCTIONS.md              # Manual completo de uso
├── 📖 DEMONSTRATION_GUIDE.md       # Guia para documentar testes
│
├── 🧪 test_local.py                # Script de teste (Python - multiplataforma)
├── 🧪 test_local.sh                # Script de teste (Bash - Linux/Mac)
│
├── 📂 client-server/
│   ├── ✨ server.py                # NOVO: Servidor standalone
│   ├── ✨ client.py                # NOVO: Cliente standalone
│   └── zmq_client-server.py        # Original (execução local)
│
├── 📂 pub-sub/
│   ├── ✨ publisher.py             # NOVO: Publisher standalone
│   ├── ✨ subscriber.py            # NOVO: Subscriber standalone
│   └── zmq_pub-sub.py              # Original (execução local)
│
└── 📂 pipeline_producer-consumer/
    ├── ✨ producer.py              # NOVO: Producer standalone
    ├── ✨ worker.py                # NOVO: Worker standalone
    ├── tasksrc.py                  # Versão intermediária
    ├── taskwork.py                 # Versão intermediária
    ├── constPipe.py                # Constantes
    └── zmq_producer-worker.py      # Original (execução local)
```

## 🚀 Quick Start

### 1. Instalar Dependências

```bash
pip install pyzmq
```

### 2. Testar Localmente

```bash
# Opção 1: Python (funciona em qualquer OS)
python test_local.py

# Opção 2: Bash (Linux/Mac)
./test_local.sh
```

### 3. Executar em Máquinas Diferentes

**Exemplo: Cliente-Servidor**

**Máquina A (Servidor):**
```bash
cd client-server
python server.py 12345
```

**Máquina B (Cliente):**
```bash
cd client-server
python client.py 192.168.1.100 12345  # Use o IP da Máquina A
```

## 📚 Documentação Completa

Para instruções detalhadas sobre cada padrão e execução distribuída:

👉 **[INSTRUCTIONS.md](INSTRUCTIONS.md)** - Manual completo de uso

👉 **[DEMONSTRATION_GUIDE.md](DEMONSTRATION_GUIDE.md)** - Como documentar seus testes

## ✨ Principais Modificações

### 🔧 O que foi alterado?

1. **Separação de componentes**: Cada componente (servidor/cliente, publisher/subscriber, producer/worker) agora é um arquivo Python independente

2. **Configuração via parâmetros**: IP e porta podem ser especificados via linha de comando

3. **Binding correto**: Servidores/Publishers/Producers fazem bind em `tcp://*:porta` para aceitar conexões de qualquer IP

4. **Logs informativos**: Cada componente imprime mensagens claras sobre conexões e dados trocados

5. **Múltiplas instâncias**: Suporte para executar múltiplos clientes/subscribers/workers simultaneamente

### 🎯 Funcionalidades Novas

- ✅ Aceita IPs e portas como argumentos de linha de comando
- ✅ Validação e mensagens de erro claras
- ✅ Logs detalhados para debugging
- ✅ Estatísticas de processamento (especialmente no worker)
- ✅ Shutdown gracioso com Ctrl+C
- ✅ Scripts de teste automatizados
- ✅ Documentação completa

## 🔥 Exemplos Rápidos

### Cliente-Servidor
```bash
# Servidor
python server.py 12345

# Cliente
python client.py 192.168.1.100 12345 "Mensagem customizada"
```

### Publisher-Subscriber
```bash
# Publisher (publica a cada 3 segundos)
python publisher.py 12345 3

# Subscriber (recebe 10 mensagens)
python subscriber.py 192.168.1.100 12345 10
```

### Producer-Worker
```bash
# Producer (distribui 50 tarefas)
python producer.py 12345 50

# Worker 1
python worker.py W1 192.168.1.100:12345

# Worker 2
python worker.py W2 192.168.1.100:12345
```

## 🛠️ Troubleshooting

### Problema: Connection Refused
- Verifique se o servidor está rodando
- Confirme que o firewall permite a porta
- Valide o IP correto

### Problema: No route to host
- Verifique conectividade de rede
- Confirme que as máquinas estão na mesma rede

### Problema: Subscribers não recebem mensagens
- Aguarde alguns segundos após conectar
- Verifique o filtro de subscrição

**Para mais soluções, consulte [INSTRUCTIONS.md](INSTRUCTIONS.md)**

## 📦 Requisitos

- Python 3.6+
- pyzmq
- Múltiplas máquinas (ou terminais para teste local)
- Conectividade de rede entre as máquinas

## 🎓 Contexto Acadêmico

Este é um trabalho da disciplina de Sistemas Distribuídos baseado em:

- **Livro:** Tanenbaum & van Steen (2025) - Distributed Systems
- **Framework:** ZeroMQ (ØMQ)
- **Padrões:** Request-Reply, Pub-Sub, Pipeline

## 👨‍💻 Autor

Rafael Taveira
- GitHub Classroom: [Link para a tarefa](https://classroom.github.com/a/wa7oHGos)

## 📄 Licença

Uso acadêmico - Sistemas Distribuídos

---

## ✅ Checklist de Entrega

- [ ] Código funciona localmente (`test_local.py`)
- [ ] Código funciona em máquinas diferentes
- [ ] Firewall configurado
- [ ] Screenshots/logs das execuções distribuídas
- [ ] README atualizado
- [ ] Repositório commitado no GitHub Classroom
- [ ] URL do repositório postada no campo da tarefa

---

**Para começar, leia:** [INSTRUCTIONS.md](INSTRUCTIONS.md)
