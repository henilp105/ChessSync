import redis
from dotenv import load_dotenv
import os

load_dotenv()

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
secret_key = os.getenv('SECRET_KEY')

r = redis.Redis(
  host=redis_host,
  port=11111,
  password=secret_key)

