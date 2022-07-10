from fastapi import FastAPI, HTTPException

import aioredis

from os import getenv

app = FastAPI()

r = aioredis.from_url(f"redis://{getenv('REDIS_HOST')}")

@app.get("/keepalive")
async def keepalive():
    response = await r.ping()
    if response != True:
        raise HTTPException(status_code=500, detail="Redis ded")
    return response

@app.get("/stream/ajos")
async def ajo_stream(count: int = 50, id: int = 0):
    ajos = await r.xread({"ajobus": id}, count)
    return ajos

@app.get("/player/{player_id}")
async def get_player(player_id):
    ajos = await r.zscore("lb", player_id)
    return {"player_id": ajos}

@app.get("/leaderboard")
async def leaderboard():
    lb = await r.zrange("lb", 0, -1, withscores=True, desc=True)
    lb_slice = lb[:10]
    ids = []
    result = {}
    for player_tuple in lb_slice:
        id,_ = player_tuple
        ids.append(id)
    name_list = await r.mget(ids.__iter__())

    i = 0
    for player_tuple in lb_slice:
        id,amount = player_tuple
        result[id] = {"amount": int(amount), "name": name_list[i]}
        i += 1

    return result
