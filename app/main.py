from fastapi import FastAPI, Response
from sel.screenshot import make_screenshot
from minio_S3.minio import minio_upload, minio_request
from io import BytesIO
import db.db as db
import hashlib
import time
import random


def generate_hash() -> str:
    unique_str = f"{time.time()}{random.random()}"
    hash_obj = hashlib.sha256()
    hash_obj.update(unique_str.encode('utf-8'))
    return hash_obj.hexdigest()


app = FastAPI()


@app.get('/')
async def get_screenshot(url: str, is_fresh: bool) -> Response:
    if is_fresh or db.get_screenshot(url=url) is None:
        filename = f"{generate_hash()}.png"
        img_data = make_screenshot(url)
        img_file = BytesIO(img_data)
        img_file.seek(0)
        minio_upload(filename, img_file, 'image/png')
        img_file.close()
        if db.get_screenshot(url=url) is None:
            db.new_screenshot(url, filename)
        else:
            db.edit_screenshot(filename, url=url)

    elif not is_fresh:
        img_obj = db.get_screenshot(url=url)
        print(img_obj)
        img_data = minio_request(img_obj.filename)
        img_data = img_data.read()

    return Response(content=img_data, media_type='image/png')
