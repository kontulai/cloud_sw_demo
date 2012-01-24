import unittest
import tempfile
from os import path
from BonkCache import BonkCache

class TestBonkCache(unittest.TestCase):

    db = path.join(tempfile.gettempdir(), 'bonk.db')

    def setUp(self):
        self.cache = BonkCache(self.db)

    def test_create_bonk_cache(self):
        self.assertEquals(self.cache.read(0), ('OK',0))

    def test_increase(self):
        self.assertEquals(self.cache.increase(1), ('OK',1))
        self.assertEquals(self.cache.read(0), ('OK',1))

    def test_decrease(self):
        self.assertEquals(self.cache.increase(1), ('OK',1))
        self.assertEquals(self.cache.decrease(1), ('OK',0))

    def test_increase_combinations(self):
        self._inc(0, 1, 'OK', 1, 1)
        self._inc(0, 0, 'ERROR', 0, 0)
        self._inc(250, 20, 'OK', 255, 255)
        self._inc(255, 20, 'ERROR', 255, 255)
        self._inc(3, 7, 'OK', 10, 10)
        self._inc(25, 0, 'ERROR', 25, 25)

    def _inc(self, start_value, inc, result, result_value, db_value):
        self.cache._save_value(start_value)
        status, value = self.cache.increase(inc)
        self.assertEquals((status, value), (result, result_value))
        self.assertEquals(self.cache._read_value(), db_value)

    def test_decrease_combinations(self):
        self._dec(1, 1, 'OK', 0, 0)
        self._dec(0, 1, 'ERROR', 0, 0)
        self._dec(5, 20, 'ERROR', 5, 5)
        self._dec(7, 3, 'OK', 4, 4)
        self._dec(20, 0, 'OK', 20, 20)

    def _dec(self, start_value, inc, result, result_value, db_value):
        self.cache._save_value(start_value)
        status, value = self.cache.decrease(inc)
        self.assertEquals((status, value), (result, result_value))
        self.assertEquals(self.cache._read_value(), db_value)

    def test_read(self):
        self.cache._save_value(0)
        self.assertEquals(self.cache.read(0), ('OK', 0))
        self.cache._save_value(45)
        self.assertEquals(self.cache.read(0), ('OK', 45))
        self.cache._save_value(255)
        self.assertEquals(self.cache.read(0), ('OK', 255))

    def test_read_fails_with_value(self):
        self.assertRaises(Exception, self.cache.read, 1)
        self.assertRaises(Exception, self.cache.read, 255)


if __name__ == "__main__":
    unittest.main()