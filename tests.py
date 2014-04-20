import unittest
import simplejson as json
from client import CacheClient
from entity import CachedEntity


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

    def test_set_and_get_dict(self):

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

    def test_set_and_get_obj(self):

        class Person(CachedEntity):

            def __init__(self, id, name, age, lastname, job):

                self.id = id
                self.name = name
                self.age = age
                self.lastname = lastname
                self.job = job

                CachedEntity.__init__(self)

            def get_id(self):

                return self.id

        person = Person("person-1", "juan", 25, "garcia", "developer")

        self.assertEquals(True, person.save())

        data = Person.get(person.id)

        self.assertEquals(data, person.get_attrs())
        self.assertEquals(True, person.delete(person.id))


unittest.main()