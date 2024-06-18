from pydantic import BaseModel


class Annotation(BaseModel):
    annotationId: int | None = None
    imageId: int
    classId: int
    cxNorm: float
    cyNorm: float
    wNorm: float
    hNorm: float