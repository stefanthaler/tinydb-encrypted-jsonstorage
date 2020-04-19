import unittest

from unittest import TestCase
from os.path import join as join_path
from tinydb import TinyDB

import tinydb_encrypted_jsonstorage as tae
import os


PATH =join_path(".",".test-reflect.db")
KEY = "test"
def a_function():
    pass

class TestPassword(unittest.TestCase):

    def setUp(self):
        self.db = TinyDB(encryption_key=KEY, path=PATH, storage=tae.EncryptedJSONStorage)

    def tearDown(self):
        self.db.close()
        os.remove(PATH)

    def test_db_cannot_be_opened_with_wrong_key(self):
        self.db.close()
        with self.assertRaises(ValueError, msg="Wrong password should not work "):
            db = TinyDB(encryption_key="OTHERKEY", path=PATH, storage=tae.EncryptedJSONStorage)

    def test_password_can_be_changed(self):
        inserted_values = {"a":"1","b":"2"}
        self.db.insert(inserted_values)
        self.db.storage.change_encryption_key("NEW_KEY")

        with self.assertRaises(ValueError, msg="Wrong password should not work "):
            db = TinyDB(encryption_key="OTHERKEY", path=PATH, storage=tae.EncryptedJSONStorage)

        read_data = self.db.all()[0]
        self.assertEqual(read_data,inserted_values, "After password change DB should contain original data")

        self.db.close()
        re_opened_db = TinyDB(encryption_key="NEW_KEY", path=PATH, storage=tae.EncryptedJSONStorage)
        self.assertIsNotNone(re_opened_db,"you should be able to reopen the database with new password")
        read_data = re_opened_db.all()[0]
        self.assertEqual(read_data,inserted_values, "After reopening, the database should still contain original values")
        re_opened_db.close()
