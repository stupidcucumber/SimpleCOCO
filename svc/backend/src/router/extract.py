from fastapi import APIRouter

router = APIRouter(
    prefix='/extract'
)


@router.get('/classes')
def post_classes(datasetName: str, id: int | None = None):
    pass


@router.get('/images')
def post_images(datasetName: str, id: int | None = None):
    pass


@router.get('/annotations')
def post_annotations(image_id: int):
    pass
