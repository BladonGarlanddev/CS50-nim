from nim import train, play
import redis
import json 

r = redis.Redis(host="localhost", port="6379", db=0)
data = None

def store(key, data):
    try:
        if isinstance(data, dict):
            data = {str(k): v for k, v in data.items()}

        serialized = json.dumps(data)
        result = r.set(key, serialized)
        return result
    except TypeError as te:
        print(f"Failed to serialize data (unsupported type): {te}")
        print(f"key: {key}")
        return False
    except redis.RedisError as re:
        print(f"Redis error occurred: {re}")
        return False


def retrieve(key):
    data = r.get(key)
    if data:
        return json.loads(data)

    return None


try:
    data = retrieve("data")
    if data:
        print(f"data recieved with len: {len(data)}")
    else:
        print(f"Data empty")

except redis.RedisError as re:
    print(f"error retrieving data: {re}")

except Exception as e:
    print(f"error retrieving data: {e}")

ai = train(0, data)

if not data:
    try:
        store("data", ai.q)
    except Exception as e: 
        print(f"An error occurred: {str(e)}")

play(ai)
