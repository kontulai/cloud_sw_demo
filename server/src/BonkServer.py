import threading
import SocketServer


class BonkServer(object):

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._server = None

    def start(self):
        self._server = BonkServerThreading((self._ip, self._port), BonkRequestHandler)
        server_thread = threading.Thread(target=self._server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def stop(self):
        self._server.shutdown()


class BonkRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        self.request.send('\xff')


class BonkServerThreading(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    allow_reuse_address = True
