import pathlib
import base64


def image2base64(image_path: pathlib.Path) -> str:
    with image_path.open('rb') as image_f:
        result = base64.b64encode(image_f.read()).decode()
    return result


def base64tobytes(base64_str: str) -> bytes:
    return base64.b64decode(base64_str)