from packet_handler import Packet


class AwkPacket(Packet):
    """
    Awknowledge: Packet used to awknowledge requests
    """

    def __init__(self):
        pass

    def handle(self, connection):
        pass

    def to_bytes(self) -> bytes:
        pass

    @classmethod
    def from_bytes(cls, payload: bytes):
        return cls()
