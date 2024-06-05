import requests
from ...backend.src.structs import (
    Annotation
)


def get_annotations(url: str, dataset_id: int) -> list[Annotation]:
    response = requests.get(
        url=url + '/extract/annotations',
        params={
            'datasetId': dataset_id
        }
    )
    response.raise_for_status()
    return [
        Annotation(**item) for item in response.json()
    ]
    
    
def post_annotation(url: str, annotation: Annotation) -> Annotation:
    response = requests.post(
        url=url + '/fill/annotation',
        json=annotation.model_dump()
    )
    response.raise_for_status()
    return Annotation(**response.json())


def update_annotation(url: str, annotation: Annotation) -> Annotation:
    pass


def delete_annotation(url: str, annotation: Annotation) -> Annotation:
    pass