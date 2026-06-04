import packet_handler as Packet


class FileBridge:
    def packet_to_file(self, packet: Packet, path):
        packet_bytes = packet.to_bytes()

        packetID = Packet.packetHandler.class_to_id[packet.class_id]
        packetLength = len(packet_bytes)
        packetHeader = Packet.PacketHeader(packetID, packetLength)

        packetTrailer = Packet.PacketTrailer()
        packetTrailer.create_crc(packet_bytes)

        data = Packet.encode(
            header=packetHeader, payload=packet, trailer=packetTrailer
        )

        with open(path, "wb") as file:
            file.write(data)

    # TODO: def file_to_packet(self, path: str):
