import threading
import SocketServer
import tempfile
from os import path

from BonkCache import BonkCache

# 1: Does not listen for connections
# 2: Responds with 0xffff to all requests
# 3: Does not support increasing and decreasing
# 4. Does not support decreasing
# 5. Read request with value will cause a crash
# 6. All works(?)
VERSION = 1

class BonkServer(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    INCREASE = '\x01'
    DECREASE = '\x02'
    READ = '\x03'

    OK = '\x01' 
    ERROR = '\x02'
    UNKNOWN = '\x03'

    db = path.join(tempfile.gettempdir(), 'bonk.db')

    def __init__(self, ip, port):
        self._ip = ip
        self._port = int(port)
        self._server = None

    def start(self):
        if VERSION == 1:
            return
        self._server = BonkServerThreading((self._ip, self._port), BonkRequestHandler)
        self._server.init_cache(self.db)
        server_thread = threading.Thread(target=self._server.serve_forever, args=(0.1,))
        server_thread.daemon = True
        server_thread.start()

    def stop(self):
        if VERSION == 1:
            return
        self._server.shutdown()

    def write_db(self, value):
        with open(self.db, 'wb') as db:
            db.write(chr(int(value)))

    def read_db(self):
        with open(self.db, 'rb') as db:
            return ord(db.read())


class BonkRequestHandler(SocketServer.BaseRequestHandler):

    rc_map = {'OK': BonkServer.OK,
              'ERROR': BonkServer.ERROR,
              'UNKNOWN': BonkServer.UNKNOWN}

    def handle(self):
        if self.server.crashed:
            return
        data = self.request.recv(1024)
        if VERSION == 2:
            self.request.send('\xff\xff')
        if len(data) != 2:
            #print 'Illegal request: %s\n' % repr(data)
            return
        req, value = data[0], ord(data[1])
        rc, return_value = self._execute_command(req, value)
        self.request.send(self.rc_map[rc]+chr(return_value))

    def _execute_command(self, req, value):
        if req == BonkServer.INCREASE and VERSION > 3:
            rc, return_value = self.server.cache.increase(value)
        elif req == BonkServer.DECREASE and VERSION > 4:
            rc, return_value = self.server.cache.decrease(value)
        elif req == BonkServer.READ:
            if value and VERSION < 6:
                self.server.crashed = True
                print 'BONK SERVER CRASH!!!'
            rc, return_value = self.server.cache.read()
        else:
            rc, return_value = 'UNKNOWN', 0
        return rc, return_value


class BonkServerThreading(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

    def init_cache(self, db):
        self.cache = BonkCache(db)
        self.crashed = False
