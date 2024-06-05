from pydantic import BaseModel


class Class(BaseModel):
    classId: int | None = None
    datasetId: int
    className: str