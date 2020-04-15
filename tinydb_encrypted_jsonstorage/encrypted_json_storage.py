from tinydb.storages import Storage, touch
from typing import Dict, Any, Optional
import json
import os
from os.path import join as join_path
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
import shutil
import sys
import traceback
import shutil
from tinydb import TinyDB

class EncryptedJSONStorage(Storage):
    """
    Store the data in a JSON file.
    """

    def __init__(self, encryption_key,  path: str, create_dirs=True, encoding=None, **kwargs):
        """
        Create a new instance.
        Also creates the storage file, if it doesn't exist.
        :param path: Where to store the JSON data.
        :param encryption_key The encryption / decryption key
        """

        super().__init__()

        # create db if not exists
        touch(path, create_dirs=create_dirs)  # Create file if not exists

        self.kwargs = kwargs

        h = SHA256.new()
        h.update(str.encode(encryption_key))
        self.encryption_key = h.digest()
        self._handle = open(path, 'rb+', encoding=encoding)
        self.encoding = encoding
        self.path=path
        self.chunk_size=64

    def close(self) -> None:
        self._handle.close()

    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:
        # Get the file size
        self._handle.seek(0, os.SEEK_END)
        size = self._handle.tell()

        if not size:
            # File is empty
            return None
        else:
            # load IV

            self._handle.seek(0)
            IV = self._handle.read(16)

            # load message_size
            db_size = self._handle.read(16)
            if (len(db_size)==0):
                return None
            db_size = int(db_size)
            # decrypt data
            crypt =  AES.new(self.encryption_key, AES.MODE_CBC, IV)
            decrypted_chunks = [b""]*( int(db_size/self.chunk_size) + 1 )
            for i in range(0,db_size,self.chunk_size):
                decrypted_chunks[int(i/self.chunk_size)] = crypt.decrypt(self._handle.read(self.chunk_size))

            decrypted_db = b"".join(decrypted_chunks)

            if len(decrypted_db)==0:
                return None

            # parse json
            return json.loads(decrypted_db.decode("utf-8"))

    def write(self, data: Dict[str, Dict[str, Any]]):
        # backup old db
        shutil.copyfile(self.path, self.path+"_backup")

        try:

            touch(self.path, False)  # create database file

            # write IV
            self._handle.seek(0)
            #''.join(chr(random.randint(0, 0xFF))
            IV = Random.new().read(16)
            self._handle.write(IV)

            # serialize and encrypt DB
            message = json.dumps(data, **self.kwargs)
            message_size = str(len(message)).zfill(16).encode("ascii")
            self._handle.write(message_size)

            crypt = AES.new(self.encryption_key, AES.MODE_CBC, IV)

            for i in range(0, len(message), self.chunk_size):

                chunk = message[i:i+self.chunk_size]
                if len(chunk) % self.chunk_size != 0:
                    chunk += ' ' * (self.chunk_size - len(chunk) % self.chunk_size)
                self._handle.write(crypt.encrypt(str.encode(chunk)))

            # flush DB
            self._handle.flush()
            os.fsync(self._handle.fileno())
            self._handle.truncate()
        except:

            print("WARNING: could not write database: ", sys.exc_info()[0])
            shutil.copyfile(self.path+"_backup", self.path)
            traceback.print_tb(sys.exc_info()[2])
            0/0
        finally:
            os.remove(self.path+"_backup")


    def change_encryption_key(self, new_encryption_key):
        new_db_path = self.path + "_clone"

        try:
            db_new_pw = TinyDB(encryption_key=new_encryption_key, path=new_db_path, storage=EncryptedJSONStorage)

        except:
            print("Error opening database with new password, aborting.", sys.exc_info()[0])
            print("Error: ", sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            return False

        try:
            # copy from old to new
            self._handle.flush()
            db_new_pw.storage.write(self.read())
            self._handle.close()

            # copy new over old
            shutil.copyfile(new_db_path, self.path)

            # reset encryption handle
            self.encryption_key=new_encryption_key
            h = SHA256.new()
            h.update(str.encode(self.encryption_key))
            self.encryption_key = h.digest()
            self._handle = open(self.path, 'rb+', encoding=self.encoding)

            success=True
        except:
            print("WARNING: could not write database: ", sys.exc_info()[0])
            print("Error: ", sys.exc_info()[1])
            traceback.print_tb(sys.exc_info()[2])
            success=False
        finally:
            os.remove(new_db_path)
        return success
