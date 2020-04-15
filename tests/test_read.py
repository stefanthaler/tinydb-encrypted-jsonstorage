import unittest

from unittest import TestCase
from os.path import join as join_path
from tinydb import TinyDB

import tinydb_encrypted_jsonstorage as tae
import os


PATH =join_path(".",".test-reflect.db")
KEY = "test"

class TestRead(unittest.TestCase):


    def setUp(self):
        self.db = TinyDB(encryption_key=KEY, path=PATH, storage=tae.EncryptedJSONStorage)

    def tearDown(self):
        self.db.close()
        os.remove(PATH)

    def test_data_can_be_read(self):
        

        pass
        # data can be read
