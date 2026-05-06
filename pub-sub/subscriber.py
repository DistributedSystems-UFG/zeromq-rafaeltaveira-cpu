#!/usr/bin/env python3
"""
ZeroMQ Publish-Subscribe Pattern: Subscriber
Este subscriber pode se conectar a um publisher em outra máquina.
Múltiplos subscribers podem se conectar ao mesmo publisher.

Uso:
    python subscriber.py <publisher-ip> [porta] [num_mensagens] [filtro]
    
Exemplos:
    python subscriber.py localhost                      # conecta em localhost:12345, recebe 5 msgs
    python subscriber.py 192.168.1.100                  # conecta em 192.168.1.100:12345
    python subscriber.py 192.168.1.100 5555            # conecta em 192.168.1.100:5555
    python subscriber.py 192.168.1.100 5555 10         # recebe 10 mensagens
    python subscriber.py 192.168.1.100 5555 10 "TIME"  # filtra por "TIME"
"""
import zmq
import sys

def subscriber(publisher_ip, port=12345, num_messages=5, filter_prefix="TIME"):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)          # create a subscriber socket
    
    # Connect to the publisher (can be on a different machine)
    publisher_address = f"tcp://{publisher_ip}:{port}"
    print(f"[SUBSCRIBER] Connecting to {publisher_address}...")
    socket.connect(publisher_address)
    
    # Subscribe to messages with specified filter
    socket.setsockopt(zmq.SUBSCRIBE, filter_prefix.encode())
    print(f"[SUBSCRIBER] Subscribed to messages starting with: '{filter_prefix}'")
    print(f"[SUBSCRIBER] Waiting for {num_messages} messages...")
    
    for i in range(num_messages):
        message = socket.recv()  # receive a message related to subscription
        print(f"[SUBSCRIBER] Message {i+1}/{num_messages}: {message.decode()}")
    
    socket.close()
    context.term()
    print("[SUBSCRIBER] Subscriber finished.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python subscriber.py <publisher-ip> [porta] [num_mensagens] [filtro]")
        print("Example: python subscriber.py 192.168.1.100 12345 5 TIME")
        sys.exit(1)
    
    publisher_ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
    num_messages = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    filter_prefix = sys.argv[4] if len(sys.argv) > 4 else "TIME"
    
    subscriber(publisher_ip, port, num_messages, filter_prefix)
