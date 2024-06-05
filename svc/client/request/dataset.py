import requests


def get_datasets(url: str) -> list[str]:
    response = requests.get(url=url + '/extract/datasets', params={})
    return response.json()['datasets']


def post_dataset(url: str, name: str, description: str) -> None:
    response = requests.post(
        url=url + '/datasets/insert',
        json={
            'datasetName': name,
            'datasetDescription': description
        }
    )
    return response.json()