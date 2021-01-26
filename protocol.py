class Packet:
    id = int()

    def decode(self, buffer: bytes):
        self.id = int.from_bytes(buffer, "big", signed=False)

    def encode(self) -> bytes:
        buffer = bytes()
        buffer += self.id.to_bytes(length=4, byteorder="big", signed=False)
        return buffer

    # should return a packet to be sent back in response to it...
    def handle(self):
        return self


class Message(Packet):
    id = 0

    msg = str()

    def decode(self, buffer: bytes):
        self.msg = buffer.decode(encoding='utf-8')

    def encode(self) -> bytes:
        return bytes(self.msg, encoding='utf-8')

    def handle(self):
        return False


class PromptResponse(Packet):
    id = 2

    data = str()

    def decode(self, buffer: bytes):
        self.data = buffer.decode(encoding='utf-8')

    def encode(self) -> bytes:
        return bytes(self.data, encoding='utf-8')

    def handle(self):
        return False


class Prompt(Packet):
    id = 1

    message = str()

    def decode(self, buffer: bytes):
        self.message = buffer.decode(encoding='utf-8')

    def encode(self) -> bytes:
        return bytes(self.message, encoding='utf-8')

    def handle(self):
        p = PromptResponse()
        p.data = input(self.message)
        return p


class PacketPool:
    pool = {}

    def __init__(self):
        self.register(Prompt())
        self.register(PromptResponse())

    def register(self, packet: Packet) -> None:
        self.pool[packet.id] = packet

    def unregister(self, pid: int) -> None:
        self.pool.pop(pid)

    def get_packet(self, pid: int) -> Packet:
        return self.pool[pid]
