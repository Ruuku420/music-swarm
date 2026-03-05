from client import client

from packets.pex import PEXPacket
from packets.ping import PingPacket


class Peer:
    def __init__(self, addr):
        self.id_ = addr
        self.connection = None

        self.data = None

    def __str__(self):
        return self.id_

    def __eq__(self, other):
        """
        Allows `in` checks without connections confounding whether or not the
        id is found in a Peer.
        """

        return self.id_ == other.id_

    def send_ping(self):
        packet = PingPacket()
        self.connection.send(packet)

    def send_pex(self, peer_list):
        address_list = [peer.id_ for peer in client.peers]
        packet = PEXPacket(address_list)
        self.connection.send(packet)
