import requests


def upload_image(url: str, dataset_id: int, image_type_id: int, 
                 image_name: str, image_base64: str) -> dict:
    response = requests.post(
        url=url + '/images/insert',
        json={
            'datasetId': dataset_id,
            'imageTypeId': image_type_id,
            'imageName': image_name,
            'imageBase64': image_base64
        }
    )
    return response.json()


def download_images(url: str, dataset_id: int, page_size: int, page_number: int) -> list:
    return requests.get(
        url=url + '/images/extract',
        params={
            'dataset_id': dataset_id,
            'pageSize': page_size,
            'pageNumber': page_number
        }
    ).json()