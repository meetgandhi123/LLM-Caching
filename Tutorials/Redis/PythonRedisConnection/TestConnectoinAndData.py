import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

keys = redis_client.get('name')

print(keys)