#!/usr/bin/env python3
"""
ZeroMQ Pipeline Pattern: Producer (Task Ventilator)
Este producer distribui tarefas para múltiplos workers que podem estar em máquinas diferentes.

Uso:
    python producer.py [porta] [num_tasks]
    
Exemplos:
    python producer.py                  # porta 12345, 100 tarefas
    python producer.py 5678            # porta 5678, 100 tarefas
    python producer.py 5678 50         # porta 5678, 50 tarefas
"""
import zmq
import time
import pickle
import sys
import random

def producer(port=12345, num_tasks=100):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)      # create a push socket
    
    # Bind to all interfaces to accept connections from workers
    bind_address = f"tcp://*:{port}"
    socket.bind(bind_address)
    print(f"[PRODUCER] Listening on {bind_address}")
    print(f"[PRODUCER] Workers should connect to: tcp://<this-machine-ip>:{port}")
    print(f"[PRODUCER] Will distribute {num_tasks} tasks")
    print("[PRODUCER] Press Enter to start distributing tasks...")
    input()
    
    print(f"[PRODUCER] Starting to distribute {num_tasks} tasks...")
    start_time = time.time()
    
    for i in range(num_tasks):
        workload = random.randint(1, 100)     # compute workload (milliseconds)
        print(f"[PRODUCER] Task {i+1}/{num_tasks}: workload={workload:3d}ms")
        socket.send(pickle.dumps(workload))   # send workload to worker
        time.sleep(0.001)  # small delay to allow fair distribution
    
    elapsed = time.time() - start_time
    print(f"\n[PRODUCER] All {num_tasks} tasks distributed in {elapsed:.2f} seconds")
    print("[PRODUCER] Workers will continue processing. Press Ctrl+C to stop.")
    
    try:
        # Keep producer alive so workers can finish
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[PRODUCER] Shutting down...")
    finally:
        socket.close()
        context.term()
        print("[PRODUCER] Producer stopped.")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    num_tasks = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    print(f"Starting producer on port {port}...")
    producer(port, num_tasks)
