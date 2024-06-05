from pydantic import BaseModel


class Image(BaseModel):
    datasetId: int
    imageData: str


class GeneratedImage(Image):
    imageId: int | None = None


class BackgroundImage(Image):
    backgroundId: int | None = None
    
    
class ForegroundImage(Image):
    foregroundId: int | None = None