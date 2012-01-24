from __future__ import with_statement

class BonkCache(object):

    def __init__(self, db_file):
        self._db_file = db_file
        self._save_value(0)

    def read(self):
        return ('OK', self._read_value())

    def increase(self, value):
        current = self._read_value()
        new_value = self._read_value() + value
        if value < 1:
            return ('ERROR', current)
        if current > 254:
            return ('ERROR', current)
        if new_value > 255:
            new_value = 255
        self._save_value(new_value)
        return ('OK', new_value)

    def decrease(self, value):
        current = self._read_value()
        new_value = current - value
        if new_value < 0:
            return ('ERROR', current)
        self._save_value(new_value)
        return ('OK', new_value)

    def _save_value(self, value):
        with open(self._db_file, 'wb') as db:
            db.write(chr(value))

    def _read_value(self):
        with open(self._db_file, 'rb') as db:
            return ord(db.read())