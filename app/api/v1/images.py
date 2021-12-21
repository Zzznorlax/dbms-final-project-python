import requests

from typing import Any
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services import auth as auth_service
from app.utils import auth as auth_utils
from app.utils.config import get_settings, Settings

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def upload_image(
    *,
    config: Settings = Depends(get_settings),
    token: str = Depends(auth_utils.oauth2_scheme),
    file: UploadFile = File(...)
) -> Any:
    """
    Upload image
    """

    auth_service.verify_jwt(config, token)

    headers = {
        'Authorization': "Client-ID {}".format(config.IMGUR_API_CLIENT_ID),
    }

    files = {
        'image': file.file,
    }

    resp = requests.post(config.IMGUR_API_URL, headers=headers, files=files)

    resp = resp.json()
    if not resp.get('success'):
        raise HTTPException(500, "upload image failed")

    data = resp.get('data')
    return {
        'data': {
            'url': data.get('link')
        }
    }
