import sys

sys.path.append("../")
from source.core import s3, stable_diffusion
from source.core.config import config
import boto3
import requests
import io
from uuid import uuid4
from PIL import Image

bucket = config.stable_diffusion_bucket
key = config.stable_diffusion_key
key_path = f"{key}/{uuid4()}.png"
expires_in = config.expires_in

client_action = "get_object"  # ['get', 'put_object']

# # 'Key' 에는 파일 이름이 들어가야한다.
url = s3.generate_presigned_url(
    client_action, {"Bucket": bucket, "Key": key_path}, expires_in
)
print(f"GET URL: {url}")
prompt = "a surfer is riding a horse on the beach"

pil_image = stable_diffusion.create_image(prompt)

s3.upload_image(pil_image, bucket, key_path, FORMAT="PNG")


# print(url)
# print("Putting data to the URL.")
# try:
#     response = requests.put(url, data="object_text")
# except FileNotFoundError:
#     print(f"Couldn't find. For a PUT operation, the key must be the "
#             f"name of a file that exists on your computer.")
