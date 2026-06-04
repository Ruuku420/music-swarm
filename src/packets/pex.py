from packet_handler import Packet

from client import client


class PEXPacket(Packet):
    """
    Peer Exchange: Packet used to send an receive swarm peer list
    """

    def __init__(self, address_list):
        # List<Tuple<Str, Int>>
        self.address_list = address_list

    def handle(self, connection):
        client.peers_from_list(self.address_list)

    def to_bytes(self) -> bytes:
        address_binary_list = []
        for address in self.address_list:
            hostname = bytes(address[0], "utf-8")
            port = address[1].to_bytes(2, "big")
            address_binary_list.append(hostname + port)
            # Append a delimiter?

        data = b"".join(address_binary_list)
        return data

    @classmethod
    def from_bytes(cls, payload: bytes):
        # TODO: Deserialize address_list
        address_list = payload
        return cls(address_list)
