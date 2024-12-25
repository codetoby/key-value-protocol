import socket
from common import Payload, RequestType, Header

def construct_payload(message : str) -> Payload:
    parts: list[str] = message.split(" ")
    type: RequestType = RequestType.from_string(parts[0])
    data: str = " ".join(parts[1:])
    return Payload(Header(type, len(data)), data)

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  
    server_port = 8000  

    client.connect((server_ip, server_port))

    try:
        while True:
            msg = input("Enter message: ")
            payload = construct_payload(msg)
            client.sendall(payload.to_bytes())

            response = client.recv(1024)
            response = response.decode("utf-8")

            print(f"Received: {response}")
    except KeyboardInterrupt:
        client.close()


run_client()
