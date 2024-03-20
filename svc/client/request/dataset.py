import requests


def get_datasets(url: str) -> list[str]:
    response = requests.get(url=url + '/datasets/extract', params={})
    return response.json() 


def post_dataset(url: str, type_id: int, name: str, description: str) -> None:
    response = requests.post(
        url=url + '/datasets/insert',
        json={
            'datasetTypeId': type_id,
            'datasetName': name,
            'datasetDescription': description
        }
    )
    return response.json()