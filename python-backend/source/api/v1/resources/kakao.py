from fastapi import APIRouter, status, BackgroundTasks
from loguru import logger
from source.schema import kakao
from source.core import kakao_api


router = APIRouter()


@router.post("/message", status_code=status.HTTP_200_OK, response_model=kakao.KakaoAPI)
async def message(request: kakao.KakaoAPI, background_tasks: BackgroundTasks):

    logger.debug(f'MESSAGE REQUEST: {request}')
    try:
        return kakao_api.parse_request(request, background_tasks)
    except Exception as e:
        logger.error(f"ERROR: {e}")
        return kakao_api.send_message("잘못된 요청입니다")
