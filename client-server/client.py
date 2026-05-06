#!/usr/bin/env python3
"""
ZeroMQ Request-Reply Pattern: Client
Este cliente pode se conectar a um servidor em outra máquina.

Uso:
    python client.py <server-ip> [porta] [mensagem]
    
Exemplos:
    python client.py localhost                    # conecta em localhost:12345
    python client.py 192.168.1.100                # conecta em 192.168.1.100:12345
    python client.py 192.168.1.100 5555           # conecta em 192.168.1.100:5555
    python client.py 192.168.1.100 12345 "Olá"   # envia mensagem customizada
"""
import zmq
import sys

def client(server_ip, port=12345, message="Hello world"):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)       # create request socket
    
    # Connect to the server (can be on a different machine)
    server_address = f"tcp://{server_ip}:{port}"
    print(f"[CLIENT] Connecting to {server_address}...")
    socket.connect(server_address)
    
    # Send message
    print(f"[CLIENT] Sending: {message}")
    socket.send(message.encode())             # send message
    
    # Wait for response
    response = socket.recv()                 # block until response
    print(f"[CLIENT] Received: {response.decode()}")
    
    # Tell server to stop
    print("[CLIENT] Sending STOP command...")
    socket.send(b"STOP")                    # tell server to stop
    final_response = socket.recv()
    print(f"[CLIENT] Final response: {final_response.decode()}")
    
    socket.close()
    context.term()
    print("[CLIENT] Client finished.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <server-ip> [porta] [mensagem]")
        print("Example: python client.py 192.168.1.100 12345")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
    message = sys.argv[3] if len(sys.argv) > 3 else "Hello world"
    
    client(server_ip, port, message)
