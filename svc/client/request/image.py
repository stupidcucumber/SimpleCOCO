import requests
from ...backend.src.structs import (
    GeneratedImage
)


def upload_generated_image(url: str, generated_image: GeneratedImage) -> dict:
    response = requests.post(
        url=url + '/fill/generatedImage',
        json=generated_image.model_dump()
    )
    response.raise_for_status()
    return response.json()


def get_images(url: str, dataset_id: int) -> list[GeneratedImage]:
    response = requests.get(
        url=url + '/extract/generatedImages',
        params={
            'datasetId': dataset_id
        }
    )
    response.raise_for_status()
    return [
        GeneratedImage(**item) for item in response.json()
    ]


def delete_image(url: str, generated_image: GeneratedImage):
    pass


def download_generated_images(url: str, dataset_id: int, page_size: int, page_number: int) -> list[GeneratedImage]:
    response = requests.get(
        url=url + '/extract/generatedImagesGlob',
        params={
            'datasetId': dataset_id,
            'pageSize': page_size,
            'pageNumber': page_number
        }
    )
    response.raise_for_status()
    return [GeneratedImage(**item) for item in response.json()]