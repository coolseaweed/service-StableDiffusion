
from typing import Dict, Optional, List
from pydantic import BaseModel, Field, validator


class KakaoUser(BaseModel):
    id: str
    properties: Dict
    type: str


class KakaoUserRequest(BaseModel):
    block: Dict
    lang: Optional[str]
    params: Dict
    timezone: str
    user: KakaoUser
    utterance: str


class KakaoAction(BaseModel):
    clientExtra: Optional[Dict]
    detailParams: Dict
    id: str
    name: str
    params: Dict


class KakaoAPI(BaseModel):
    """Main Kakao JSON"""

    action: KakaoAction
    bot: Dict
    contexts: Optional[List]
    intent: Dict
    userRequest: KakaoUserRequest
