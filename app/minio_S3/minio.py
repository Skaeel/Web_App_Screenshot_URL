from minio import Minio, S3Error
import os


def minio_request(object_name: str) -> None:
    bucket_name = 'mybucket'
    found = minio_client.bucket_exists(bucket_name)
    if not found:
        print(f'Bucket {bucket_name} not found')
        return
    try:
        if minio_client.stat_object(bucket_name, object_name):
            return minio_client.get_object(bucket_name, object_name)
        else:
            print(f"Object {object_name} not found in bucket {bucket_name}")
    except S3Error as e:
        print(f"Error getting image: {e}")


def minio_upload(filename: str, file_object: object, content_type: str) -> dict:
    bucket_name = 'mybucket'
    found = minio_client.bucket_exists(bucket_name)
    if not found:
        minio_client.make_bucket(bucket_name)
    else:
        print(f"Bucket {bucket_name} already exists")
    try:
        result = minio_client.put_object(bucket_name, filename, file_object,
                                         file_object.getbuffer().nbytes, content_type)
        print(f"File {filename} successfully uploaded to Minio")
        return {"filename": result.object_name}
    except S3Error as e:
        print(f"Error occurred while uploading file to Minio: {e}")
        return {"error": str(e)}


minio_root_user = os.getenv('MINIO_ROOT_USER')
minio_root_password = os.getenv('MINIO_ROOT_PASSWORD')

minio_config = {
    'endpoint': 'minio:9000',
    'access_key': f'{minio_root_user}',
    'secret_key': f'{minio_root_password}',
    'secure': False
}

minio_client = Minio(
    minio_config['endpoint'],
    access_key=minio_config['access_key'],
    secret_key=minio_config['secret_key'],
    secure=minio_config['secure']
)
