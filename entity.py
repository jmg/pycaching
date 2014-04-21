from client import CacheClient
import simplejson as json


class CachedEntity(object):

    def __init__(self):

        self._cache = CacheClient()

    def save(self):

        entity_id = self.get_id()
        data = json.dumps(self.get_attrs())

        if self._cache.set(entity_id, data):
            return entity_id

    def get_attrs(self):

        return dict([(key, value) for key, value in self.__dict__.iteritems() if not key.startswith("_")])

    @staticmethod
    def get(key):

        return json.loads(CacheClient().get(key))

    @staticmethod
    def delete(key):

        return CacheClient().delete(key)

    def get_id(self):

        return self.__hash__()

