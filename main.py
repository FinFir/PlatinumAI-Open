import json
import random
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Optional, List
import pytz
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./public"), name="static")

OPENAI_API_KEY = 'x'

MONGO_URL = os.getenv('MONGO_URI')
if not MONGO_URL:
    raise RuntimeError("MongoDB URI (MONGO_URI) environment variable is not set")
client = MongoClient(MONGO_URL)
db = client.api_management
users_collection = db.users
requests_collection = db.requests

RATE_LIMITS = {
    "basic": {"per_minute": 15, "per_day": 1000},
    "pro": {"per_minute": 60, "per_day": 5000}
}

with open('./storage/providers.json', 'r') as f:
    PROVIDERS = json.load(f)

def get_provider_url(model):
    compatible_providers = [url for url, models in PROVIDERS.items() if model in models]
    if not compatible_providers:
        raise HTTPException(status_code=400, detail="Requested model not available")
    return random.choice(compatible_providers)

def get_reset_time():
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    reset_time = now.replace(hour=13, minute=0, second=0, microsecond=0)
    if now >= reset_time:
        reset_time += timedelta(days=1)
    return reset_time

def verify_api_key(api_key: Optional[str] = None):
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key is missing")
    api_key = api_key.split("Bearer ")[-1]
    user = users_collection.find_one({"api_key": api_key})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    reset_time = get_reset_time()
    last_reset = user.get('last_reset', reset_time - timedelta(days=1))

    if now >= reset_time and last_reset < reset_time:
        users_collection.update_one(
            {"api_key": api_key},
            {"$set": {"daily_count": 0, "last_reset": reset_time}}
        )
        user['daily_count'] = 0

    minute_ago = now - timedelta(minutes=1)
    key_type = user.get("key_type", "basic")
    rate_limit = RATE_LIMITS[key_type]
    minute_count = requests_collection.count_documents({
        "api_key": api_key,
        "timestamp": {"$gte": minute_ago}
    })
    if minute_count >= rate_limit["per_minute"]:
        raise HTTPException(status_code=429, detail="Rate limit exceeded (per minute)")
    daily_count = user.get('daily_count', 0)
    if daily_count >= rate_limit["per_day"]:
        raise HTTPException(status_code=429, detail="Rate limit exceeded (per day)")
    requests_collection.insert_one({
        "api_key": api_key,
        "timestamp": now
    })
    users_collection.update_one(
        {"api_key": api_key},
        {"$inc": {"daily_count": 1}}
    )

    return user

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("./public/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.post("/v1/chat/completions")
async def proxy(request: Request):
    api_key = request.headers.get("Authorization")
    user = verify_api_key(api_key)

    headers = {
        'Content-Type': 'application/json',
    }

    body = await request.json()
    stream = body.get('stream', False)
    model = body.get('model')

    if not model:
        raise HTTPException(status_code=400, detail="Model not specified in request")

    provider_url = get_provider_url(model)

    async def stream_response(url):
        async with httpx.AsyncClient() as client:
            async with client.stream('POST', url, headers=headers, json=body, timeout=None) as response:
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail=await response.text())
                async for line in response.aiter_lines():
                    if line.strip():
                        yield f"{line}\n\n"

    if stream:
        return StreamingResponse(stream_response(provider_url), media_type="text/event-stream")
    else:
        async with httpx.AsyncClient() as client:
            response = await client.post(provider_url, headers=headers, json=body)

        if response.status_code != 200:
            compatible_providers = [url for url, models in PROVIDERS.items() if model in models]
            for url in compatible_providers:
                if url != provider_url:
                    response = await client.post(url, headers=headers, json=body)
                    if response.status_code == 200:
                        break
            else:
                raise HTTPException(status_code=400, detail="Unable to process request with any available provider")

        return StreamingResponse(iter([response.content]), media_type="application/json")

class Model(BaseModel):
    id: str
    object: str
    created: int
    owned_by: str
    type: str
    endpoint: str
    cost: int

class ModelList(BaseModel):
    object: str
    data: List[Model]

models_data = ModelList(
    object="list",
    data=[
        Model(id="gpt-3.5", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-3.5-turbo", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-4", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-4-turbo", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-4o", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-4-1106-preview", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-4-0125-preview", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-4o-2024-05-13", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-4-turbo-2024-04-09", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-4-32k", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-3.5-turbo-1106", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
        Model(id="gpt-3.5-turbo-0125", object="model", created=0, owned_by="openai", type="chat.completions", endpoint="/v1/chat/completions", cost=1),
    ]
)

@app.get("/v1/models")
async def get_models():
    return models_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
