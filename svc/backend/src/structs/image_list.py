from pydantic import BaseModel
from .image import Image


class ImageList(BaseModel):
    images: list[Image]