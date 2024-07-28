import socket
import json
import os

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def save_data(data):
    data_dir = 'machine_data'
    os.makedirs(data_dir, exist_ok=True)
    filename = f"{data['hostname']}_{data['architecture']}.json"
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server listening on', HOST, ':', PORT)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024)
            if not data:
                break
            try:
                machine_data = json.loads(data.decode())
                save_data(machine_data)
                print(f"Received data from {addr}: {machine_data}")
            except json.JSONDecodeError:
                print("Error decoding JSON data")
