class Peer:
    def __init__(self, addr):
        self.id_ = addr
        self.incoming_conn = None
        self.outgoing_conn = None

        self.data = None

    def __str__(self):
        return self.id_

    def __eq__(self, other):
        return self.id_ == other.id_

    def disconnect(self):
        raise NotImplementedError
