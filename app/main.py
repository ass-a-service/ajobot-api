from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import aioredis
import requests
from os import getenv

app = FastAPI()

r = aioredis.from_url(f"redis://{getenv('REDIS_HOST')}")
    
@app.get("/auth/discord")
async def auth_discord(code: str):
    API_ENDPOINT = 'https://discord.com/api/v10'
    CLIENT_ID = 'kok'
    CLIENT_SECRET = 'kek'
    REDIRECT_URI = 'http://localhost:8000/auth/discord'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r1 = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    r1.raise_for_status()
    result1 = r1.json()
    r2 = requests.get('%s/users/@me' % API_ENDPOINT, headers={"Authorization": f"Bearer {result1['access_token']}"})
    r2.raise_for_status()
    return r2.json()

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
        result[name_list[i]] = int(amount)
        i += 1

    return result
