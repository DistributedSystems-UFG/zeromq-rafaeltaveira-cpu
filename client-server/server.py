#!/usr/bin/env python3
"""
ZeroMQ Request-Reply Pattern: Server
Este servidor pode ser executado em uma máquina separada.
O servidor escuta em todas as interfaces de rede (0.0.0.0) na porta especificada.

Uso:
    python server.py [porta]
    
Exemplo:
    python server.py 12345
"""
import zmq
import sys

def server(port=12345):
    context = zmq.Context()
    socket = context.socket(zmq.REP)       # create reply socket
    
    # Bind to all interfaces (*) to accept connections from other machines
    bind_address = f"tcp://*:{port}"
    socket.bind(bind_address)
    print(f"[SERVER] Listening on {bind_address}")
    print(f"[SERVER] Clients should connect to: tcp://<this-machine-ip>:{port}")
    
    message_count = 0
    while True:
        message = socket.recv()               # wait for incoming message
        message_count += 1
        print(f"[SERVER] Received message #{message_count}: {message.decode()}")
        
        if "STOP" not in str(message):        # if not to stop...
            reply = str(message.decode()) + '*'   # append "*" to message
            socket.send(reply.encode())         # send it away (encoded)
            print(f"[SERVER] Sent reply: {reply}")
        else:
            print("[SERVER] Received STOP command. Shutting down...")
            socket.send(b"Server shutting down")
            break                               # break out of loop and end
    
    socket.close()
    context.term()
    print("[SERVER] Server stopped.")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
    print(f"Starting server on port {port}...")
    server(port)
