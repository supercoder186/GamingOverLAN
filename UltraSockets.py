import queue
import socket
import struct
import threading


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class ProtoSockets:
    def __init__(self, host, port):
        pass

    def protosend(self, message, conn):
        message = str(message).encode()
        conn.send(message)

    def protorecieve(self, conn):
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            return data


# noinspection PyUnresolvedReferences
class GenericSockets:
    def __init(self):
        pass

    def get(self, number_of_entries):
        if self.received.qsize() != 0:
            values = []
            if number_of_entries != "all":
                for _ in range(0, number_of_entries):
                    value = self.received.get()
                    values.append(value)
            else:
                for _ in range(0, self.received.qsize()):
                    value = self.received.get()
                    values.append(value)
            return values
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def parse_host(self, hostname):
        host = hostname.replace('tcp://', '').split(':')
        try:
            port = int(host[1])
        except IndexError:
            raise TypeError("Invalid format! Use format <ip>:<port>")
        host = host[0]
        return host, port


class Server(ProtoSockets, GenericSockets):

    def __init__(self, hostname, connections, name):

        self.users = {}
        self.type = "server"
        self.Socket = socket.socket()
        self.name = name
        self.collector_threads = []
        self.received = queue.Queue()

        host, port = self.parse_host(hostname)

        self.Socket.bind((host, port))
        self.Socket.listen(connections)

        self.handshake_initiate(connections)

    def handshake_initiate(self, connections):

        for i in range(0, connections):
            conn, addr = self.Socket.accept()
            print("Connection from: " + str(addr))
            name = self.protorecieve(conn)
            self.users[name] = [conn, addr]

            t = threading.Thread(target=self.idle_collector, args=(conn, name,))
            t.start()
            self.collector_threads.append(t)

        for key, _ in self.users.items():
            # noinspection PyUnboundLocalVariable
            self.protosend(self.name, conn)

    def idle_collector(self, conn, name):
        while True:
            while True:
                size = struct.unpack("i", conn.recv(struct.calcsize("i")))[0]
                data = ""
                while len(data) < size:
                    msg = conn.recv(size - len(data))
                    data += msg.decode()

                if not data:
                    break

                recipient = data.partition(',')

                if recipient[0] == self.name:
                    if recipient[2] == "closerequest":
                        self.send(name, "closeaccepted")
                        break
                    else:
                        self.received.put([name, recipient[2], self.received.qsize()])
                else:
                    self.send(name, recipient[2])

            restart = self.protorecieve(conn)

            if restart == "restart":
                pass
            elif restart == "terminate":
                break

    def send(self, name, message):
        message = name + ',' + str(message)
        message = struct.pack("i", len(message)) + message.encode()
        self.users[name][0].send(message)


# noinspection PyAttributeOutsideInit
class Client(ProtoSockets, GenericSockets):
    def __init__(self, hostname, name):
        self.type = "client"
        self.conn = socket.socket()
        self.name = name
        self.received = queue.Queue()

        host, port = self.parse_host(hostname)

        self.handshake_accept(host, port)

    def handshake_accept(self, host, port):
        self.conn.connect((host, port))
        self.protosend(self.name, self.conn)
        self.servername = self.protorecieve(self.conn)

        self.collect = threading.Thread(target=self.idle_collector)
        self.collect.start()

    def send(self, name, message):
        message = name + ',' + str(message)
        message = struct.pack("i", len(message)) + message.encode()
        self.conn.send(message)

    def idle_collector(self):
        conn = self.conn
        while True:
            size = struct.unpack("i", conn.recv(struct.calcsize("i")))[0]
            data = ""

            while len(data) < size:
                msg = conn.recv(size - len(data))
                data += msg.decode()

            if not data:
                break

            recipient = data.partition(',')

            if recipient[2] == 'closeaccepted':
                break
            else:
                self.received.put([recipient[0], recipient[2], self.received.qsize()])

    def close(self):
        self.send(self.servername, "closerequest")
        self.collect.join()

    def open(self):
        self.collect = threading.Thread(target=self.idle_collector)
        self.collect.start()
        self.protosend('restart', self.conn)

    def terminate(self):
        self.send(self.servername, "closerequest")
        self.protosend('terminate', self.conn)
        self.collect.join()


if __name__ == '__main__':
    print("Hello World")
