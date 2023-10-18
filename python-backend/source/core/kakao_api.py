from fastapi.responses import JSONResponse
from loguru import logger
from source.core.config import config
from source.schema import kakao
from fastapi import BackgroundTasks
from source.static.urls import url_dict
from source.core import stable_diffusion, s3
from uuid import uuid4




def keyboard(request):
    logger.info(f'KEYBOARD REQUEST: {request}')

    return JSONResponse({
        'type': 'text'
    })


def send_message(msg):
    return JSONResponse({
        'version': "2.0",
        'template': {
            'outputs': [{
                'simpleText': {'text': f"{msg}"}
            }]
        }
    })


def send_picture(url):
    return JSONResponse({
        'version': "2.0",
        'template': {
            'outputs': [{
                "simpleImage": {
                    "imageUrl": f"{url}",
                }
            }]
        }
    })



async def create_image_and_upload_to_s3(prompt:str, bucket:str, key_path:str):

    try:
        pil_image = await stable_diffusion.create_image(prompt)
        s3.upload_image(pil_image, bucket, key_path,FORMAT='PNG')
    except Exception as e:
        logger.error(f"Failed to create image -> {e}")
        raise

def parse_prompt(text:str):
    return text.replace('/prompt','').strip()

def parse_request(request: kakao.KakaoAPI, background_tasks: BackgroundTasks):

    user_uttr = request.userRequest.utterance

    if '/돌팔이' == user_uttr:
        return send_picture(url_dict['stone82'])
    
    elif '/식은김' == user_uttr:
        return send_picture(url_dict['coolseaweed'])
    
    elif user_uttr.startswith('/prompt'):
        prompt = parse_prompt(user_uttr)
        key_path = f"{config.stable_diffusion_key}/{uuid4()}.png"
        bucket = config.stable_diffusion_bucket
        tmp_image_url = s3.generate_presigned_url("get_object", {'Bucket': bucket, 'Key': key_path}, config.expires_in)
        background_tasks.add_task(create_image_and_upload_to_s3, prompt, bucket, key_path)
        
        return send_message(f"이미지를 생성중 입니다.. 약 6~10초 뒤에 아래 url을 통해 이미지를 받을 수 있습니다. 해당 url은 1시간 후 만료됩니다 :)\n{tmp_image_url}")
        
    else:
        return send_message("잘 모르겠습니다")
