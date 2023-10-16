from fastapi.responses import JSONResponse
from loguru import logger
from source.core.config import config
from source.schema import kakao
from fastapi import BackgroundTasks
from source.static.urls import url_dict


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


def parse_request(request: kakao.KakaoAPI, background_tasks: BackgroundTasks):

    user_uttr = request.userRequest.utterance

    if '/돌팔이' == user_uttr:
        return send_picture(url_dict['stone82'])
    elif '/식은김' == user_uttr:
        return send_picture(url_dict['coolseaweed'])
    else:
        return send_message("잘 모르겠습니다")
