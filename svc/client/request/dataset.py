import requests
from ...backend.src.structs import (
    Dataset
)


def get_datasets(url: str) -> list[Dataset]:
    response = requests.get(url=url + '/dataset/extract')
    response.raise_for_status()
    return [
        Dataset(**item) for item in response.json()
    ]


def post_dataset(url: str, dataset: Dataset) -> Dataset:
    response = requests.post(
        url=url + '/dataset/insert',
        json=dataset.model_dump()
    )
    response.raise_for_status()
    return response.json()