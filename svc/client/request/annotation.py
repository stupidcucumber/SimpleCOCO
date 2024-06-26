import requests
from ...backend.src.structs import (
    Annotation
)


def get_annotations(url: str, image_id: int) -> list[Annotation]:
    response = requests.get(
        url=url + '/annotation/extract',
        params={
            'imageId': image_id
        }
    )
    response.raise_for_status()
    return [
        Annotation(**item) for item in response.json()
    ]
    
    
def post_annotation(url: str, annotation: Annotation) -> int:
    response = requests.post(
        url=url + '/annotation/insert',
        json=annotation.model_dump()
    )
    response.raise_for_status()
    return response.json()


def update_annotation(url: str, annotation: Annotation) -> int:
    response = requests.put(
        url=url + '/annotation/update',
        json=annotation.model_dump()
    )
    response.raise_for_status()
    return response.json()


def delete_annotation(url: str, annotation: Annotation) -> int:
    response = requests.delete(
        url=url + '/annotation/delete',
        params={
            'id': annotation.annotationId
        }
    )
    response.raise_for_status()
    return response.json()