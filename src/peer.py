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

    def disconnect(self):
        self.connection.alive = False
        self.connection.reading_thread.join()
        self.connection.sending_thread.join()
