from rejson import  Path

class RedisJsonUtilities(object):
    def __init__(self, redis_client):
        self.client  = redis_client

    def set_key_value(self , json_key,  json_object):
        return self.client.jsonset(json_key, Path.rootPath(), json_object)

    def get_values_by_key(self , json_key , path):
        return self.client.jsonget(json_key, Path(path))

    def del_key_value(self , json_key):
        return self.client.jsondel(json_key, Path('.'))

    def append_rules_in_redis(self , json_key , path,  json_object , namespace): ## assumption to have empty rules array in the DB
        if self.get_values_by_key(json_key,'.'):
            try: 
                self.get_values_by_key(json_key,'.' + str(namespace))
            except:
                self.client.jsonset(json_key, Path('.' + str(namespace)), {})
            return self.client.jsonset(json_key, Path(path), json_object)
        
        self.set_key_value(json_key , {})
        self.client.jsonset(json_key, Path('.' + str(namespace)), {})
        return self.client.jsonset(json_key, Path(path), json_object)
