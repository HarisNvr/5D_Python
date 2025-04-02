from os import getenv
from uuid import uuid4

from redis.asyncio import Redis
from fastapi import FastAPI, HTTPException, Depends
from httpx import AsyncClient
from pydantic import BaseModel, HttpUrl
from starlette.responses import RedirectResponse

app = FastAPI()


async def get_redis() -> Redis:
    redis = Redis.from_url(
        getenv("REDIS_URL", "redis://localhost:6379"),
        decode_responses=True
    )
    return redis


class URLRequest(BaseModel):
    url: HttpUrl


@app.post("/", status_code=201)
async def shorten_url(request: URLRequest, redis=Depends(get_redis)):
    """
    Generate a short identifier for the given URL and store it in Redis.

    :return: A JSON response containing the short URL identifier.
    """

    short_id = str(uuid4())[:8]
    await redis.set(short_id, str(request.url))

    return {"short_url": short_id}


@app.get("/fetch")
async def fetch_data(url: str):
    """
    Perform an asynchronous HTTP GET request to the given URL
    and return the response.

    :return: The JSON response from the requested URL.
    """

    async with AsyncClient() as client:
        response = await client.get(url)

        return response.json()


@app.get("/storage")
async def fetch_all(redis=Depends(get_redis)):  # Kinda print() func
    """
    Retrieve all stored short URLs and their corresponding original URLs.

    :return: A JSON dictionary containing short URL identifiers as keys
             and original URLs as values.
    """

    keys = await redis.keys("*")
    urls = {key: await redis.get(key) for key in keys}

    return urls


@app.get("/{short_id}", status_code=307)
async def redirect_to_original(short_id: str, redis=Depends(get_redis)):
    """
    Redirect to the original URL based on the given short identifier.

    :return: A 307 redirect response to the original URL.
    """

    original_url = await redis.get(short_id)
    if not original_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return RedirectResponse(
        url=original_url
    )
