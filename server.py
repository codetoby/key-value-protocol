import socket
from common import Payload, Header, RequestType, Response
    
def parse_request(request : bytes) -> Payload:
    request : str = request.decode("utf-8")
    print(request)
    parts : list[str] = request.split(" ")
    if (len(parts) <= 1):
        return None
    if (parts[0] == "GET"):
        if (len(parts) != 3):
            return None
        data : str = parts[2]
        data_length : int = len(data)
        if (data_length != int(parts[1])):
            return None
        return Payload(Header(RequestType.GET, int(parts[1])), data)
    
    if (parts[0] == "SET"):
        if (len(parts) != 4):
            return None
        data : str = " ".join(parts[2:])
        data_length : int = len(data)
        header_length = int(parts[1])
        if (data_length != header_length):
            return None
        return Payload(Header(RequestType.SET, int(parts[1])), data)
    
def construct_response(response : Response) -> bytes:
    return response.to_bytes()

def handle_payload(payload : Payload) -> Response:
    if payload.header.type.value == RequestType.GET.value:
        return Response(HASHMAP.get(payload.data, "Not Found"))
    if payload.header.type.value == RequestType.SET.value:
        key, value = payload.data.split(" ")
        HASHMAP[key] = value
        return Response("Ok")
    return Response("Bad Request")

HASHMAP = {
    "name": "John Doe",
}


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    port = 8000

    server.bind((server_ip, port))

    server.listen(0)

    client_socket, client_address = server.accept()

    try:
        while True:
            request = client_socket.recv(1024)
            payload : Payload = parse_request(request)
            print(payload)
            
            if payload == None:
                response = "Error"
                client_socket.send(response.encode("utf-8"))
                continue
            
            response : Response = handle_payload(payload)
            client_socket.send(construct_response(response))
    except KeyboardInterrupt:
        client_socket.close()
        server.close()

if __name__ == "__main__":
    run_server()
