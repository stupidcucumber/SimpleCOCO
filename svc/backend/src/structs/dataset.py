from pydantic import BaseModel


class Dataset(BaseModel):
    datasetId: int | None = None
    datasetName: str
    datasetDescription: str