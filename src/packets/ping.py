from packet_handler import Packet


class PingPacket(Packet):
    """
    Ping: Testing packet
    """
    class_id = 'ping'
    
    def __init__(self):
        pass

    def handle(self, connection):
        print(f"[Host] Recieved Ping from {connection.address[0]}:{connection.address[1]}")

    def to_bytes(self) -> bytes:
        return bytes()

    @classmethod
    def from_bytes(cls, payload: bytes):
        return cls()
