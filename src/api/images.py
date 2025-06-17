from fastapi import APIRouter, UploadFile
from src.services.images import ImageService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/", summary="Загрузить изображение")
def upload_image(file: UploadFile):
    ImageService().upload_image(file)
