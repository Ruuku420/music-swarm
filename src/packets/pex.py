from packet_handler import Packet

"""
Peer Exchange: Packet used to send an receive swarm peer list
"""


class PEXPacket(Packet):
    def __init__(self, address_list):
        self.address_list = address_list

    def handle(self, connection):
        pass

    def to_bytes(self) -> bytes:
        pass

    @classmethod
    def from_bytes(cls, payload: bytes):
        return cls()
