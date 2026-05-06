#!/usr/bin/env python3
"""
ZeroMQ Pipeline Pattern: Worker (Task Worker)
Este worker pode se conectar a um ou mais producers em máquinas diferentes.
Múltiplos workers podem ser executados para processar tarefas em paralelo.

Uso:
    python worker.py <worker-id> <producer-ip>:<porta> [<producer-ip>:<porta> ...]
    
Exemplos:
    python worker.py 1 localhost:12345                          # worker 1 conecta a localhost:12345
    python worker.py 2 192.168.1.100:12345                      # worker 2 conecta a 192.168.1.100:12345
    python worker.py 3 192.168.1.100:12345 192.168.1.101:12345 # worker 3 conecta a 2 producers
"""
import zmq
import time
import pickle
import sys

def worker(worker_id, producer_addresses):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)      # create a pull socket
    
    # Connect to all specified producers
    print(f"[WORKER-{worker_id}] Connecting to producers:")
    for addr in producer_addresses:
        full_address = f"tcp://{addr}"
        socket.connect(full_address)
        print(f"[WORKER-{worker_id}]   - {full_address}")
    
    print(f"[WORKER-{worker_id}] Ready to receive tasks. Press Ctrl+C to stop.")
    
    task_count = 0
    total_workload = 0
    
    try:
        while True:
            # Receive work from any connected producer
            workload = pickle.loads(socket.recv())
            task_count += 1
            total_workload += workload
            
            print(f"[WORKER-{worker_id}] Task #{task_count}: workload={workload:3d}ms (total={total_workload}ms)")
            
            # Simulate work by sleeping (workload is in milliseconds)
            time.sleep(workload / 1000.0)
            
    except KeyboardInterrupt:
        print(f"\n[WORKER-{worker_id}] Shutting down...")
    finally:
        avg_workload = total_workload / task_count if task_count > 0 else 0
        print(f"[WORKER-{worker_id}] Statistics:")
        print(f"[WORKER-{worker_id}]   - Tasks completed: {task_count}")
        print(f"[WORKER-{worker_id}]   - Total workload: {total_workload}ms")
        print(f"[WORKER-{worker_id}]   - Average workload: {avg_workload:.2f}ms")
        socket.close()
        context.term()
        print(f"[WORKER-{worker_id}] Worker stopped.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python worker.py <worker-id> <producer-ip>:<porta> [<producer-ip>:<porta> ...]")
        print("Examples:")
        print("  python worker.py 1 localhost:12345")
        print("  python worker.py 2 192.168.1.100:12345")
        print("  python worker.py 3 192.168.1.100:12345 192.168.1.101:12345")
        sys.exit(1)
    
    worker_id = sys.argv[1]
    producer_addresses = sys.argv[2:]
    
    worker(worker_id, producer_addresses)
