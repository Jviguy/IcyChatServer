from threading import Thread
import socket
import protocol

class Member:
    addr = tuple
    conn = socket.socket

    def __init__(self, addr: tuple, conn: socket.socket):
        self.addr = addr
        self.conn = conn


class Server(Thread):
    port = int
    members = list
    pool = protocol.PacketPool()

    def __init__(self, port: int):
        super().__init__()
        self.port = port
        self.members = []

    def run(self) -> None:
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockfd.bind(('0.0.0.0', self.port))
        sockfd.listen(True)
        while True:
            connfd, addr = sockfd.accept()
            t = Thread(target=self._handle_client, kwargs={'member': Member(addr=addr, conn=connfd)})
            t.setDaemon(True)
            t.start()

    def _handle_client(self, member: Member) -> None:
        self.members.append(member)
        try:
            while True:
                data = member.conn.recv(1024)
                if not data:
                    break

            member.conn.close()
            self.members.remove(member)
        except socket.error:
            member.conn.close()
            self.members.remove(member)

    def _push_message_to_members(self, msg: str, origin: Member):
        for member in self.members:
            # Prevent the message from going back to the sender...
            if member.addr is not origin.addr:
                member.conn.sendall(bytes(msg, encoding='utf-8'))
