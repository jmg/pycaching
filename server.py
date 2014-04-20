import socket
import protocol
import logging


class CacheServer(object):

    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = socket.gethostname()
        port = 22122
        self.socket.bind((host, port))

        self.socket.listen(5)

    def send(self, message):

        protocol.send_message(self.client, message)

    def receive(self):

        return protocol.receive_message(self.client)

    def close(self):

        self.client.close()

    def server_forever(self):

        while True:

            self.client, addr = self.socket.accept()
            logging.log('Got connection from {0}'.format(addr))

            message = self.receive()
            logging.log(message)

            response = protocol.execute(message)
            self.send(response)

            self.close()


if __name__ == "__main__":
    CacheServer().server_forever()