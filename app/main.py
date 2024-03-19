from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from sel.screenshot import make_screenshot
from minio_S3.minio import minio_upload, minio_request
from io import BytesIO
from db.db import engine, async_session
import db.db as db
import hashlib
import time
import random


def generate_hash() -> str:
    unique_str = f"{time.time()}{random.random()}"
    hash_obj = hashlib.sha256()
    hash_obj.update(unique_str.encode('utf-8'))
    return hash_obj.hexdigest()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_table(engine) 
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def get_screenshot(url: str, is_fresh: bool) -> Response:
    if is_fresh or await db.get_screenshot(async_session, url=url) is None:
        filename = f"{generate_hash()}.png"
        img_data = make_screenshot(url)
        img_file = BytesIO(img_data)
        img_file.seek(0)
        minio_upload(filename, img_file, 'image/png')
        img_file.close()
        if await db.get_screenshot(async_session, url=url) is None:
            await db.new_screenshot(async_session, url, filename)
        else:
            await db.edit_screenshot(async_session, filename, url=url)

    elif not is_fresh:
        img_obj = await db.get_screenshot(async_session, url=url)
        img_data = minio_request(img_obj.filename)
        img_data = img_data.read()

    return Response(content=img_data, media_type='image/png')
