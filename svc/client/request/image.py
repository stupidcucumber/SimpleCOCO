import requests
import json


def upload_images(host: str, port: str, dataset_id: int, body: dict) -> list:
    response = requests.post(
        url='http://%s:%s/fill/images' % (str(host), str(port)), params={
            'dataset_id': dataset_id
        },
        json=body
    )
    return response.json()


def download_icons(host: str, port: str, dataset_id: int, page_size: int, page_number: int) -> list:
    response = requests.get(
        url='http://%s:%s/extract/icons' % (str(host), str(port)),
        params={
            'dataset_id': dataset_id,
            'page_size': page_size,
            'page_number': page_number
        }
    ).json()
    
    return response['images']