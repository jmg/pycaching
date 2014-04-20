import unittest
import simplejson as json
from client import CacheClient


class CacheTest(unittest.TestCase):

    def test_set(self):

        self.assertEquals(True, CacheClient().set("key-1", "test"))

    def test_get(self):

        CacheClient().set("key-1", "test")
        self.assertEquals("test", CacheClient().get("key-1"))

    def test_delete(self):

        CacheClient().set("key-1", "test")
        self.assertEquals(True, CacheClient().delete("key-1"))
        self.assertEquals(None, CacheClient().get("key-1"))

    def test_set_and_get_obj(self):

        person = {
            "id": "person-1",
            "name": "juan",
            "age": 25,
            "lastname": "garcia",
            "job": "developer",
        }

        CacheClient().set(person["id"], json.dumps(person))
        data = json.loads(CacheClient().get(person["id"]))

        self.assertEquals(data, person)


unittest.main()