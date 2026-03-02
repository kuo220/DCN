import socket
import json
from pathlib import Path
import re

AS_IP = "0.0.0.0"
AS_PORT = 53533
DATA_FILE = "data.json"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((AS_IP, AS_PORT))  # Listen on all interfaces

print("Authoritatvie server is running on port 53533...")

def parse_message(data: str) -> dict:
    pattern = r'(\w+)=([^\s\n]+)'
    matches = re.findall(pattern, data)
    return dict(matches)

def load_data() -> dict:
    data_path = Path(DATA_FILE)
    if data_path.exists():
        with open(data_path, "r") as f:
            return json.load(f)
    else:
        return {}

def save_data(data: dict):
    data_path = Path(DATA_FILE)
    with open(data_path, "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    while True:
        data, addr = server.recvfrom(2048)

        message: dict = parse_message(data.decode())

        # Registration
        if len(message) == 4:
            db = load_data()
            name = message.get("NAME")
            db[name] = message
            save_data(db)
            server.sendto(b"201", addr)
        elif len(message) == 2:
            db = load_data()
            name: str = message.get("NAME")
            record: dict = db.get(name, {})
            response = f"TYPE={record['TYPE']}\nNAME={record['NAME']} VALUE={record['VALUE']} TTL={record['TTL']}"
            server.sendto(response.encode(), addr)