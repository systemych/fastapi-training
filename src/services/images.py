import shutil
from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import resize_image

class ImageService(BaseService):
    def upload_image(file: UploadFile):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image(image_path)