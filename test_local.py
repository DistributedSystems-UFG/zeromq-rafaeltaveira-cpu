#!/usr/bin/env python3
"""
Script de teste para validar todos os padrões ZeroMQ localmente.
Funciona em Linux, Windows e Mac.

Uso:
    python test_local.py
"""
import subprocess
import time
import sys
import os

# Cores para output (funciona em terminais que suportam ANSI)
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_colored(message, color=Colors.NC):
    """Imprime mensagem colorida"""
    print(f"{color}{message}{Colors.NC}")

def check_dependencies():
    """Verifica se pyzmq está instalado"""
    print("Verificando dependências...")
    try:
        import zmq
        print_colored("[OK] pyzmq instalado", Colors.GREEN)
        return True
    except ImportError:
        print_colored("[ERRO] pyzmq não está instalado!", Colors.RED)
        print("Execute: pip install pyzmq")
        return False

def run_test(test_name, test_dir, server_cmd, client_cmd, wait_time=2):
    """
    Executa um teste de padrão ZeroMQ
    """
    print_colored(f"\n=== Testando: {test_name} ===", Colors.YELLOW)
    print(f"Diretório: {test_dir}")
    
    # Mudar para diretório de teste
    original_dir = os.getcwd()
    os.chdir(test_dir)
    
    try:
        # Iniciar servidor/publisher/producer em background
        print("Iniciando servidor/publisher/producer...")
        server_process = subprocess.Popen(
            server_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Aguardar servidor iniciar
        time.sleep(wait_time)
        
        # Executar cliente/subscriber/worker
        print("Executando cliente/subscriber/worker...")
        client_process = subprocess.run(
            client_cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        
        # Parar servidor
        server_process.terminate()
        try:
            server_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            server_process.kill()
        
        # Verificar resultado
        if client_process.returncode == 0:
            print_colored(f"[SUCESSO] {test_name} funcionou!", Colors.GREEN)
            return True
        else:
            print_colored(f"[FALHA] {test_name} falhou!", Colors.RED)
            if client_process.stderr:
                print(f"Erro: {client_process.stderr}")
            return False
            
    finally:
        # Voltar ao diretório original
        os.chdir(original_dir)

def test_producer_worker():
    """Teste especial para Producer-Worker com múltiplos workers"""
    test_name = "Producer-Worker"
    test_dir = "pipeline_producer-consumer"
    
    print_colored(f"\n=== Testando: {test_name} ===", Colors.YELLOW)
    print(f"Diretório: {test_dir}")
    
    original_dir = os.getcwd()
    os.chdir(test_dir)
    
    try:
        # Iniciar producer
        print("Iniciando producer...")
        producer_cmd = "python producer.py 12347 10"
        producer_process = subprocess.Popen(
            producer_cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(2)
        
        # Enviar Enter para iniciar distribuição
        producer_process.stdin.write(b"\n")
        producer_process.stdin.flush()
        
        # Iniciar 3 workers
        print("Iniciando workers...")
        workers = []
        for i in range(1, 4):
            worker_cmd = f"python worker.py W{i} localhost:12347"
            worker_process = subprocess.Popen(
                worker_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            workers.append(worker_process)
        
        # Aguardar processamento
        print("Processando tarefas...")
        time.sleep(8)
        
        # Parar todos os processos
        print("Encerrando processos...")
        producer_process.terminate()
        for worker in workers:
            worker.terminate()
        
        # Aguardar encerramento
        try:
            producer_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            producer_process.kill()
        
        for worker in workers:
            try:
                worker.wait(timeout=2)
            except subprocess.TimeoutExpired:
                worker.kill()
        
        print_colored(f"[SUCESSO] {test_name} funcionou!", Colors.GREEN)
        return True
        
    except Exception as e:
        print_colored(f"[FALHA] {test_name} falhou!", Colors.RED)
        print(f"Erro: {e}")
        return False
    finally:
        os.chdir(original_dir)

def main():
    """Função principal"""
    print("=" * 50)
    print("Teste Local dos Padrões ZeroMQ")
    print("=" * 50)
    print()
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    results = []
    
    # Teste 1: Cliente-Servidor
    results.append(run_test(
        "Cliente-Servidor",
        "client-server",
        "python server.py 12345",
        "python client.py localhost 12345",
        wait_time=2
    ))
    
    # Teste 2: Pub-Sub
    results.append(run_test(
        "Publisher-Subscriber",
        "pub-sub",
        "python publisher.py 12346 2",
        "python subscriber.py localhost 12346 3",
        wait_time=2
    ))
    
    # Teste 3: Producer-Worker
    results.append(test_producer_worker())
    
    # Resumo
    print()
    print("=" * 50)
    total = len(results)
    passed = sum(results)
    
    if passed == total:
        print_colored(f"Todos os {total} testes passaram! ✓", Colors.GREEN)
    else:
        failed = total - passed
        print_colored(f"{passed}/{total} testes passaram, {failed} falharam", Colors.YELLOW)
    
    print("=" * 50)
    print()
    print("Próximos passos:")
    print("1. Testes locais OK? Agora teste em máquinas diferentes")
    print("2. Consulte INSTRUCTIONS.md para instruções detalhadas")
    print("3. Configure firewall nas máquinas (se necessário)")
    print()
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
