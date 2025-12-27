from abc import ABC, abstractmethod

class PacketHeader:
    PACKET_HEADER_SIZE = 1

    def __init__(self, id_: int = None):
        self.id = id_

    def to_bytes(self) -> bytes:
        return self.id.to_bytes(self.PACKET_HEADER_SIZE, "big")

    def from_bytes(self, header):
        id_ = header
        self.id = id_

class Packet(ABC):
    @abstractmethod
    def handle(self, peer):
        raise NotImplementedError

    @abstractmethod
    def to_bytes(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def from_bytes(self, payload):
        raise NotImplementedError

# Better to use an Enum
class PacketHandler:
    def __init__(self):
        self._current_id = 1
        self.id_to_class = {}
        self.class_to_id = {}

    def registerPacket(self, packetClass):
        packetID = self._current_id
        packetClass.header = PacketHeader(packetID)
        self.id_to_class[packetID] = packetClass
        self.class_to_id[packetClass] = packetID
        self._current_id += 1
