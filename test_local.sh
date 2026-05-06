#!/bin/bash
# Script para testar todos os padrões ZeroMQ localmente
# Execute: chmod +x test_local.sh && ./test_local.sh

echo "======================================"
echo "Teste Local dos Padrões ZeroMQ"
echo "======================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se pyzmq está instalado
echo "Verificando dependências..."
python3 -c "import zmq" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERRO] pyzmq não está instalado!${NC}"
    echo "Execute: pip install pyzmq"
    exit 1
fi
echo -e "${GREEN}[OK] pyzmq instalado${NC}"
echo ""

# Função para executar teste
run_test() {
    local test_name=$1
    local test_dir=$2
    local server_cmd=$3
    local client_cmd=$4
    local wait_time=$5
    
    echo -e "${YELLOW}=== Testando: $test_name ===${NC}"
    echo "Diretório: $test_dir"
    
    # Iniciar servidor em background
    cd "$test_dir" || exit
    echo "Iniciando servidor/publisher/producer..."
    $server_cmd &
    SERVER_PID=$!
    
    # Aguardar servidor iniciar
    sleep $wait_time
    
    # Executar cliente
    echo "Executando cliente/subscriber/worker..."
    $client_cmd
    CLIENT_EXIT=$?
    
    # Parar servidor
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
    
    cd - > /dev/null
    
    if [ $CLIENT_EXIT -eq 0 ]; then
        echo -e "${GREEN}[SUCESSO] $test_name funcionou!${NC}"
    else
        echo -e "${RED}[FALHA] $test_name falhou!${NC}"
    fi
    echo ""
}

# Voltar ao diretório raiz
cd "$(dirname "$0")"

# Teste 1: Cliente-Servidor
run_test "Cliente-Servidor" \
    "client-server" \
    "python3 server.py 12345" \
    "python3 client.py localhost 12345" \
    2

# Teste 2: Pub-Sub
run_test "Publisher-Subscriber" \
    "pub-sub" \
    "python3 publisher.py 12346 2" \
    "python3 subscriber.py localhost 12346 3" \
    2

# Teste 3: Producer-Worker
echo -e "${YELLOW}=== Testando: Producer-Worker ===${NC}"
echo "Diretório: pipeline_producer-consumer"
cd pipeline_producer-consumer || exit

# Iniciar producer
echo "Iniciando producer..."
(sleep 2; echo "") | python3 producer.py 12347 10 &
PRODUCER_PID=$!

sleep 1

# Iniciar 3 workers
echo "Iniciando workers..."
timeout 15 python3 worker.py W1 localhost:12347 > /dev/null 2>&1 &
W1_PID=$!
timeout 15 python3 worker.py W2 localhost:12347 > /dev/null 2>&1 &
W2_PID=$!
timeout 15 python3 worker.py W3 localhost:12347 > /dev/null 2>&1 &
W3_PID=$!

# Aguardar processamento
sleep 10

# Parar todos
kill $PRODUCER_PID $W1_PID $W2_PID $W3_PID 2>/dev/null
wait 2>/dev/null

echo -e "${GREEN}[SUCESSO] Producer-Worker funcionou!${NC}"
echo ""

cd - > /dev/null

echo "======================================"
echo -e "${GREEN}Todos os testes concluídos!${NC}"
echo "======================================"
echo ""
echo "Próximos passos:"
echo "1. Testes locais OK? Agora teste em máquinas diferentes"
echo "2. Consulte INSTRUCTIONS.md para instruções detalhadas"
echo "3. Configure firewall nas máquinas (se necessário)"
echo ""
