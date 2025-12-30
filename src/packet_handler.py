from abc import ABC, abstractmethod
import zlib

# from enum import Enum


class Serializable(ABC):
    @abstractmethod
    def to_bytes(self) -> bytes:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_bytes(cls, payload: bytes):
        raise NotImplementedError


class PacketHeader(Serializable):
    PACKET_HEADER_SIZE = 1

    PACKET_ID_SIZE = 1
    PACKET_LENGTH_SIZE = 0

    def __init__(self, packet_id: int, packet_length: int):
        self.packet_id = packet_id
        self.packet_length = packet_length

    def to_bytes(self) -> bytes:
        return self.packet_id.to_bytes(self.PACKET_HEADER_SIZE, "big")

    @classmethod
    def from_bytes(cls, payload):
        packet_id = payload[cls.PACKET_ID_SIZE - 1]
        packet_length = 0
        return cls(packet_id, packet_length)


class PacketTrailer(Serializable):
    # from zlib import crc32
    # can be 28 bytes if b''? Valid concern

    PACKET_TRAILER_SIZE = 32

    PACKET_CHECKSUM_SIZE = 32

    def __init__(self, crc):
        self.crc = crc

    def to_bytes(self) -> bytes:
        return self.packet_id.to_bytes(self.PACKET_TRAILER_SIZE, "big")

    @classmethod
    def from_bytes(cls, payload):
        crc = payload
        return cls(crc)

    def verify(self, payload):
        if self.crc == zlib.crc32(payload):
            return
        else:
            raise RuntimeError("Checksum of packet doesn't match")


class Packet(ABC, Serializable):
    @abstractmethod
    def handle(self, peer):
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


def encode(
    *, header: PacketHeader, payload: Packet, trailer: PacketTrailer
) -> bytearray:
    data = bytearray()
    data.extend(header.to_bytes())
    data.extend(payload.to_bytes())
    data.extend(trailer.to_bytes())
    return data
