import requests
import json
import socket
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci_service():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    print(hostname, fs_port, number, as_ip, as_port)
    if not all([hostname, fs_port, number, as_ip, as_port]) or not number.isdigit():
        return abort(400, 'Invalid request format')
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(json.dumps({'hostname': hostname, 'type': "A"}).encode(), 
                      (as_ip, int(as_port)))
    dns_response, client_address = udp_socket.recvfrom(2048)
    dns_info = json.loads(dns_response.decode())
    file_server_url = f"http://{dns_info['ip']}:{fs_port}/fibonacci?number={number}"
    return requests.get(file_server_url).text
app.run(host='0.0.0.0', port=8080, debug=True)
