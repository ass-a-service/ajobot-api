from fastapi import FastAPI
from redis import Redis
from os import getenv

app = FastAPI()

r = Redis(host=getenv('REDIS_HOST'))

@app.get("/leaderboard")
async def leaderboard():
    lb = r.zrange("lb", 0, -1, withscores=True)
    ids = []
    result = {}
    for player_tuple in lb:
        id,_ = player_tuple
        ids.append(id)
    name_list = r.mget(ids.__iter__())

    i = 0
    for player_tuple in lb:
        _,amount = player_tuple
        result[name_list[i]] = amount
        i += 1

    return result
