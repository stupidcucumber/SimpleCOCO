import requests
from ...backend.src.structs import Class


def get_classes(url: str, dataset_id: int) -> list[Class]:
    response = requests.get(
        url=url + '/class/extract',
        params={
            'datasetId': dataset_id
        }
    )
    response.raise_for_status()
    return [
        Class(**item) for item in response.json()
    ]
    
    
def post_class(url: str, class_: Class) -> Class:
    response = requests.post(
        url=url + '/class/insert',
        json=class_.model_dump()
    )
    response.raise_for_status()
    return Class(**response.json())