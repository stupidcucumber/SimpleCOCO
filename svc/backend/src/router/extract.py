from fastapi import APIRouter
from psycopg2._psycopg import connection

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


@router.get('/images')
def get_images(datasetName: str, id: int | None = None):
    pass


@router.get('/annotations')
def get_annotations(image_id: int):
    pass
