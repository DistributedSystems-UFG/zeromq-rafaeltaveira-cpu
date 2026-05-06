#!/usr/bin/env python3
"""
ZeroMQ Publish-Subscribe Pattern: Publisher
Este publisher pode ser executado em uma máquina separada.
O publisher publica mensagens que podem ser recebidas por múltiplos subscribers.

Uso:
    python publisher.py [porta] [intervalo_segundos]
    
Exemplos:
    python publisher.py                    # porta 12345, intervalo 5s
    python publisher.py 5555              # porta 5555, intervalo 5s
    python publisher.py 5555 2            # porta 5555, intervalo 2s
"""
import zmq
import time
import sys

def publisher(port=12345, interval=5):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)          # create a publisher socket
    
    # Bind to all interfaces to accept connections from other machines
    bind_address = f"tcp://*:{port}"
    socket.bind(bind_address)
    print(f"[PUBLISHER] Publishing on {bind_address}")
    print(f"[PUBLISHER] Subscribers should connect to: tcp://<this-machine-ip>:{port}")
    print(f"[PUBLISHER] Publishing interval: {interval} seconds")
    print("[PUBLISHER] Press Ctrl+C to stop")
    
    message_count = 0
    try:
        while True:
            time.sleep(interval)                    # wait specified seconds
            message_count += 1
            t = "TIME " + time.asctime()
            socket.send(t.encode())                 # publish the current time
            print(f"[PUBLISHER] Published message #{message_count}: {t}")
    except KeyboardInterrupt:
        print("\n[PUBLISHER] Shutting down...")
    finally:
        socket.close()
        context.term()
        print("[PUBLISHER] Publisher stopped.")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"Starting publisher on port {port} with {interval}s interval...")
    publisher(port, interval)
