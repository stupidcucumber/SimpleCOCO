import requests


def get_dataset_names(url: str) -> list[str]:
    response = requests.get(url=url, params={})
    names = response.json()
    print(names)
    return names['datasets']


def post_dataset(url: str, name: str) -> None:
    response = requests.post(
        url=url,
        params={
            'name': name
        }
    )
    return response.json()