from flask import Flask, request
import socket
import requests

US_PORT = 8080
FS_PORT = 9090

app = Flask(__name__)

def parse_message(data: str) -> dict:
    result: dict = {}
    for line in data.strip().split('\n'):
        for part in line.split():
            if '=' in part:
                key, value = part.split('=', 1)
                result[key] = value
    return result

@app.route('/fibonacci', methods=['GET'])
def user_server():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if hostname == '' or fs_port == '' or as_ip == '' or as_port == '' or number == '' or not number.isdigit():
        return "Bad format", 400

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Query AS
    message = f"TYPE=A\nNAME={hostname}"
    client.sendto(message.encode(), (as_ip, int(as_port)))

    # Send message to FS
    data, addr = client.recvfrom(2048)
    message: dict = parse_message(data.decode())

    fs_path = f"http://{message['VALUE']}:{FS_PORT}/fibonacci?number={number}"
    response = requests.get(fs_path)
    return response.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=US_PORT, debug=True)