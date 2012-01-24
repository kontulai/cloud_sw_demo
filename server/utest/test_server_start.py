import unittest

from BonkServer import BonkServer
from Network import TCPClient

class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = BonkServer('127.0.0.1', 55555)
        self.server.start()
        self.client = TCPClient(timeout=1)
        self.client.connect_to('127.0.0.1', 55555)

    def tearDown(self):
        self.server.stop()

    def test_server_responds_to_read_request(self):
        self.client.send(BonkServer.READ+'\x00')
        response = self.client.read()
        self.assertEquals(response, BonkServer.OK+'\x00')

    def test_server_responds_to_inc_request(self):
        self.client.send(BonkServer.INCREASE+'\x0f')
        response = self.client.read()
        self.assertEquals(response, BonkServer.OK+'\x0f')

    def test_db_access(self):
        self.assertEquals(self.server.read_db(), 0)
        self.server.write_db(5)
        self.assertEquals(self.server.read_db(), 5)

    def test_errors(self):
        self.server.write_db(255)
        self.client.send(BonkServer.INCREASE+'\x0f')
        response = self.client.read()
        self.assertEquals(response, BonkServer.ERROR+'\xff')


if __name__ == '__main__':
    unittest.main()