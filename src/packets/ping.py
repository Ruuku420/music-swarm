from packet_handler import Packet


class PingPacket(Packet):
    """
    Ping: Testing packet
    """

    def __init__(self):
        pass

    def handle(self, connection):
        print("Recieved Ping")

    def to_bytes(self) -> bytes:
        return bytes()

    @classmethod
    def from_bytes(cls, payload: bytes):
        return cls()
