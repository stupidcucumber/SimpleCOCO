from fastapi import APIRouter

router = APIRouter(
    prefix='/fill'
)

@router.post('/classes')
def post_classes():
    pass


@router.post('/images')
def post_images():
    pass


@router.post('/annotations')
def post_annotations():
    pass
