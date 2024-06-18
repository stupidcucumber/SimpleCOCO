from pydantic import BaseModel


class Image(BaseModel):
    datasetId: int
    imageDataBase64: str


class GeneratedImage(Image):
    imageId: int | None = None


class BackgroundImage(Image):
    backgroundId: int | None = None
    
    
class ForegroundImage(Image):
    foregroundId: int | None = None
    classId: int
    maskDataBase64: str