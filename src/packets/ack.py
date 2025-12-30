from packet_handler import Packet

"""
Awknowledge: Packet used to awknowledge requests
"""


class AwkPacket(Packet):
    def __init__(self):
        pass

    def handle(self, connection):
        pass

    def to_bytes(self) -> bytes:
        pass

    @classmethod
    def from_bytes(cls, payload: bytes):
        return cls()
