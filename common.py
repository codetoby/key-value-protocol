from dataclasses import dataclass
from enum import Enum

@dataclass
class RequestType(Enum):
    GET = 0
    SET = 1
    
    @staticmethod
    def from_string(s: str) -> 'RequestType':
        if s == "GET":
            return RequestType.GET
        if s == "SET":
            return RequestType.SET
        raise ValueError(f"Invalid type: {s}")

@dataclass
class Header:
    type: RequestType
    length: int
    
@dataclass
class Payload:
    header: Header
    data: str
    
    def to_bytes(self):
        return self.header.type.name.encode("utf-8") + b" " + str(self.header.length).encode("utf-8") + b" " + self.data.encode("utf-8")
    
@dataclass
class Response:
    data: str
    
    def to_bytes(self):
        return self.data.encode("utf-8")
    
    @staticmethod
    def from_bytes(data: bytes) -> 'Response':
        return Response(data.decode("utf-8"))

    
    