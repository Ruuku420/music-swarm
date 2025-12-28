from abc import ABC, abstractmethod

# from enum import Enum


class PacketHeader:
    PACKET_HEADER_SIZE = 1

    def __init__(self):
        self.packet_id = None
        """"Ts in bytes fam"""
        self.packet_length = None

        # TODO HOW THE FUCK FORMATTING
        # Maybe calculate them manually?
        self._PACKET_ID_SIZE: int = 1
        self._PACKET_LENGTH_SIZE: int = 0

    def to_bytes(self) -> bytes:
        return self.packet_id.to_bytes(self.PACKET_HEADER_SIZE, "big")

    def from_bytes(self, header):
        self.packet_id = header[self._PACKET_ID_SIZE]


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


packetHandler = PacketHandler()
