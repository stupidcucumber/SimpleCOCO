import requests


def get_dataset_types(url: str) -> list:
    return requests.get(url=url + '/datasetTypes/extract', params={}).json()