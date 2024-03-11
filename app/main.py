from fastapi import FastAPI, Response
from fastapi.exceptions import HTTPException
from sel.screenshot import make_screenshot, save_screenshot, delete_screenshot
from minio_S3.minio import minio_upload, minio_request
import db.db as db
import os
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
        if not (os.path.exists('screenshots') or os.path.isdir('screenshots')):
            os.mkdir('screenshots')
        path_to_img = os.path.join('screenshots', filename)
        try:
            save_screenshot(img_data, path_to_img)
        except Exception:
            raise HTTPException(500, 'Error occurred while saving screenshot')
        minio_upload(filename, path_to_img, 'image/png')
        delete_screenshot(path_to_img)
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
