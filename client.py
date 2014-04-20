import socket
import protocol
import logging


class CacheClient(object):

    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 22122

        self.socket.connect((host, port))

    def send(self, message):

        protocol.send_message(self.socket, message)

    def receive(self):

        response = protocol.receive_message(self.socket)
        logging.log(response)
        return response

    def close(self):

        self.socket.close()

    def get(self, key):

        self.send(protocol.build_message("GET", key))
        response = self.receive()
        if response == str(None):
            return None

        return response

    def set(self, key, data):

        self.send(protocol.build_message("SET", key, data))
        return self.receive() == "ok"

    def delete(self, key):

        self.send(protocol.build_message("DELETE", key))
        return self.receive() == "ok"