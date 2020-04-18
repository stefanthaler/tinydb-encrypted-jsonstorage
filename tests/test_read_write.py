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

class TestReadWrite(unittest.TestCase):


    def setUp(self):
        self.db = TinyDB(encryption_key=KEY, path=PATH, storage=tae.EncryptedJSONStorage)

    def tearDown(self):
        self.db.close()
        os.remove(PATH)

    def test_storage_should_be_of_correct_type(self):
        self.assertIsInstance(self.db.storage, tae.EncryptedJSONStorage)

    #  check what happens if file is wrong
    # test what happens when encrytpion key is wrong 

    def test_data_can_be_written_and_read(self):
        inserted_values = {"a":"1","b":"2"}
        self.db.insert(inserted_values)

        read_data = self.db.all()[0]
        self.assertEqual(read_data,inserted_values, "Read data should be equal to inserted data")
        # data can be read

    def test_stored_data_is_untouched_if_write_error_occurs(self):
        inserted_values = {"a":"1","b":"2"}
        self.db.insert(inserted_values)

        self.db.insert({"a":a_function}) # Functions are illegal

        read_data = self.db.all()[0]
        self.assertEqual(read_data,inserted_values, "Writing illegal data shout not cause the database to be altered")
