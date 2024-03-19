from fastapi import APIRouter
from psycopg2._psycopg import connection
from ..utils.database import extract_images

router = APIRouter(
    prefix='/extract'
)

db_connection = None
def set_connection(_connection: connection) -> None:
    global db_connection
    db_connection = _connection

@router.get('/datasets')
def get_datasets(id: int | None = None):
    result = {}
    with db_connection.cursor() as cursor:
        if id:
            cursor.execute('SELECT * FROM datasets WHERE id = %s;', (id,))
            result = {
                'datasets': cursor.fetchone()
            }
        else:
            cursor.execute('SELECT * FROM datasets;')
            result = {
                'datasets': cursor.fetchall()
            }
    return result


@router.get('/classes')
def get_classes(datasetName: str, id: int | None = None):
    pass

@router.get('/icons')
def get_icons(dataset_id: str, page_size: int, page_number: int):
    with db_connection.cursor() as cursor:
        images = extract_images(dataset_id=dataset_id, cursor=cursor)
    print(len(images), flush=True)
    result = images[page_size * page_number:page_size*(page_number+1)]
    return {
        'images': result
    }

@router.get('/images')
def get_images(dataset_id: str):
    pass

@router.get('/annotations')
def get_annotations(image_id: int):
    pass
