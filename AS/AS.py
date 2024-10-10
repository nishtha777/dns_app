import requests
import socket
import json

udp_port = 53533

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', udp_port))

while True:
    received_data, client_addr = udp_socket.recvfrom(2048)
    decoded_message = json.loads(received_data.decode())

    if len(decoded_message) != 2:
        entry = {decoded_message["NAME"]: decoded_message}
        json_entry = json.dumps(entry)
        with open("storage.json", "w") as json_file:
            json_file.write(json_entry)
        udp_socket.sendto(str(201).encode(), client_addr)
    else:
        with open("storage.json", "r") as json_file:
            stored_data = json.load(json_file)
        response_data = json.dumps(stored_data[decoded_message["NAME"]])
        udp_socket.sendto(response_data.encode(), client_addr)
