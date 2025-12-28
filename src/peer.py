class Peer:
    def __init__(self, addr):
        self.id_ = addr
        self.incoming_socket = None
        self.outgoing_socket = None

        self.data = None

    def __str__(self):
        return self.id_

    def __eq__(self, other):
        return self.id_ == other.id_
