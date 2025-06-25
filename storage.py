import redis
import os
import json
import numpy as np
from dotenv import load_dotenv

class RedisStorage:
    def __init__(self):
        load_dotenv()
        self.redis = redis.StrictRedis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            username=os.getenv("REDIS_USER"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=False
        )

    def store_image(self, image_path, image_array, expire=10):
        self.redis.setex('caminho_imagem_original', expire, image_path.encode('utf-8'))
        self.redis.setex('matriz_imagem_original', expire, image_array.tobytes())
        self.redis.setex('forma_matriz_original', expire, json.dumps(image_array.shape).encode('utf-8'))
        self.redis.setex('dtype_matriz_original', expire, str(image_array.dtype).encode('utf-8'))
