from store import storage


def build_message(action, key, data=None):

    message = "{0} {1}".format(action, key)
    if data is not None:
        message = "{0} {1}".format(message, data)

    return message


def parse(message):

    parts = message.split(" ", 2)

    action = parts[0]
    key = parts[1]
    data = parts[2] if len(parts) > 2 else None

    return action, key, data


def execute(message):

    action, key, data = parse(message)

    def get():
        return storage.get(key, str(None))

    def set():
        storage[key] = data
        return "ok"

    def delete():
        storage.pop(key, None)
        return "ok"

    actions = {
        "GET": get,
        "SET": set,
        "DELETE": delete,
    }

    return actions[action]()


EOF = "\n"

def send_message(socket, message):

    socket.sendall("{0}{1}".format(message, EOF))


def receive_message(socket):

    return socket.makefile().readline().replace(EOF, "")