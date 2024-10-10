import requests
import json
import socket
from flask import Flask, request

app = Flask(__name__)
@app.route('/fibonacci')
def handle_fibonacci():
    input_number = int(request.args.get('number'))
    return str(calculate_fibonacci(input_number))

def calculate_fibonacci(input_number):
    if input_number > 2:
        return calculate_fibonacci(input_number - 2) + calculate_fibonacci(input_number - 1)

    elif input_number == 2 or input_number == 1:
        return 1

    elif input_number == 0:
        return 0

    else:
        return 'Invalid input'
@app.route('/register')
def register_service():
    hostname = request.args.get('hostname')
    ip = request.args.get('ip')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    registration_data = {
        "TYPE": "A",
        "NAME": hostname,
        "VALUE": ip,
        "TTL": 10
    }
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(json.dumps(registration_data).encode(), (as_ip, int(as_port)))
    print('Data sent to authoritative server')

    response_code, client_addr = udp_socket.recvfrom(2048)
    decoded_code = response_code.decode('utf-8')

    if decoded_code != '201':
        return 'Error'
    else:
        return str(201)

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
