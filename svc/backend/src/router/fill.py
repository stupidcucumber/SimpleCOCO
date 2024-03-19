from fastapi import APIRouter
from psycopg2._psycopg import connection, Binary
from ..structs import Image

router = APIRouter(
    prefix='/fill'
)
db_connection = None
def set_connection(_connection: connection) -> None:
    global db_connection
    db_connection = _connection


@router.post('/dataset')
def post_dataset(name: str):
    with db_connection.cursor() as cursor:
        cursor.execute('INSERT INTO datasets (dataset_name) VALUES (%s);', (name, ))
        id = cursor.lastrowid
    db_connection.commit()
    return {
        'id': id,
        'name': name
    }

@router.post('/classes')
def post_classes():
    pass


@router.post('/images')
def post_images(imageList: list[Image], dataset_id: int):
    values = []
    for image_data in imageList:
        image_bytes = image_data.bytes.encode()
        values.append((dataset_id, image_bytes))

    with db_connection.cursor() as cursor:
        cursor.executemany(
            '''
            INSERT INTO images (dataset_id, image_data) VALUES (%s, %s);
            ''', values
        )
    db_connection.commit()
    return 200


@router.post('/annotations')
def post_annotations():
    pass
