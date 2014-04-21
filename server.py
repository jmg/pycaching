import socket
import protocol
import logging
from threading import Thread


class CacheServer(object):

    _instance = None
    run = True

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            cls._instance = super(CacheServer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = socket.gethostname()
        port = 22122
        self.socket.bind((host, port))
        logging.log("Running on {0}:{1}".format(host, port))

        self.socket.listen(5)

    def serve_forever(self):

        while CacheServer.run:

            client_thread = ClientThread(self.socket.accept())
            client_thread.start()

    def serve_forever_in_a_thread(self):

        thread = Thread(target=self.serve_forever)
        thread.start()


class ClientThread(Thread):

    def __init__(self, (client, address)):

        Thread.__init__(self)
        self.client = client
        self.address = address

    def send(self, message):

        protocol.send_message(self.client, message)

    def receive(self):

        return protocol.receive_message(self.client)

    def close(self):

        self.client.close()

    def run(self):

        logging.log('Got connection from {0}'.format(self.address))

        message = self.receive()
        logging.log(message)

        response = protocol.execute(message)
        self.send(response)

        self.close()


if __name__ == "__main__":

    CacheServer().serve_forever()