import unittest
from BonkServer import BonkServer
from Network import TCPClient

class TestServer(unittest.TestCase):

    def test_server_responds_to_request(self):
        server = BonkServer('127.0.0.1', 55555)
        server.start()
        client = TCPClient(timeout=1)
        client.connect_to('127.0.0.1', 55555)
        client.send('\xff\x00')
        response = client.read()
        self.assertTrue(response)
        server.stop()

if __name__ == '__main__':
    unittest.main()