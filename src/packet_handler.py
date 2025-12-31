from abc import ABC, abstractmethod
import zlib
import math

# from enum import Enum


class Serializable(ABC):
    @abstractmethod
    def to_bytes(self) -> bytes:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_bytes(cls, payload: bytes):
        raise NotImplementedError


# TODO
PACKET_ID_SIZE = math.ceil((127).bit_length() / 7)  # u8 int limit for # of ids
PACKET_LENGTH_SIZE = math.ceil((1024**2).bit_length() / 7)  # 1 mb

PACKET_HEADER_SIZE = PACKET_ID_SIZE + PACKET_LENGTH_SIZE


class PacketHeader(Serializable):
    def __init__(self, packet_id: int, packet_length: int):
        self.packet_id = packet_id
        self.packet_length = packet_length

    def to_bytes(self) -> bytes:
        data = bytes(
            self.packet_id.to_bytes(self.PACKET_ID_SIZE)
            + self.packet_length.to_bytes(self.PACKET_LENGTH_SIZE)
        )
        return data

    @classmethod
    def from_bytes(cls, payload):
        packet_id = payload[cls.PACKET_ID_SIZE - 1]
        packet_length = 0
        return cls(packet_id, packet_length)


PACKET_CHECKSUM_SIZE = 4  # idk how to prove this but
PACKET_TRAILER_SIZE = PACKET_CHECKSUM_SIZE


class PacketTrailer(Serializable):
    def __init__(self, crc):
        self.crc = crc

    def to_bytes(self) -> bytes:
        pass

    @classmethod
    def from_bytes(cls, payload):
        crc = payload
        return cls(crc)

    # Better abstraction?
    def create_crc(self, payload: bytes):
        self.crc = zlib.crc32(payload)

    def verify(self, payload: bytes):
        if int.from_bytes(self.crc) == zlib.crc32(payload):
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


def encode(*, header: PacketHeader, payload: Packet, trailer: PacketTrailer) -> bytes:
    data = bytes(header.to_bytes() + payload.to_bytes() + trailer.to_bytes())
    return data
