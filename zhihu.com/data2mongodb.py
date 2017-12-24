import redis
from pymongo import MongoClient
import json

# 连接数据库
redis_cli = redis.Redis(host='192.168.1.112', port=6379, db=0)

mongo_cli = MongoClient('127.0.0.1', 27017)
db = mongo_cli['zhihu']
col = db['user']

while 1:
    try:
        source, data = redis_cli.blpop(['zhihu:items'])
        # print(source)

        dict_data = json.loads(data.decode())
        # print(dict_data)

        col.insert(dict_data)
    except Exception as e:
        print(e)
    

