from flask import Flask, request
import socket

FS_PORT = 9090

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = request.get_json()
    hostname: str = data.get('hostname')
    ip: str = data.get('ip')
    as_ip: str = data.get('as_ip')
    as_port: str = data.get('as_port')

    message = f"TYPE=A\nNAME={hostname} VALUE={ip} TTL=10"
    client.sendto(message.encode(), (as_ip, int(as_port)))
    return "201"

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    n: str = request.args.get('number')
    try:
        n: int = int(n)
    except (TypeError, ValueError):
        return "Bad format", 400
    return str(fib(n)), 200

def fib(n: int) -> int:
    if n < 0:
        return 0
    if n == 1 or n == 2:
        return 1
    return fib(n-1) + fib(n-2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=FS_PORT, debug=True)