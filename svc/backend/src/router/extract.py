from fastapi import APIRouter
from psycopg2._psycopg import connection
from ..structs import (
    GeneratedImage,
    ForegroundImage,
    BackgroundImage,
    Annotation,
    Class,
    Dataset
)

router = APIRouter(
    prefix='/extract'
)

db_connection = None
def set_connection(_connection: connection) -> None:
    global db_connection
    db_connection = _connection


@router.get('/datasets')
def get_datasets() -> list[Dataset]:
    result: list[Dataset] = []
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM datasets;')
        raw_result = cursor.fetchall()
        result = [
            Dataset(
                datasetId=item[0],
                datasetName=item[1],
                datasetDescription=item[2]
            ) for item in raw_result
        ]
    return result


@router.get('/classes')
def get_classes(datasetId: int) -> list[Class]:
    result: list[Class] = []
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM classes WHERE dataset_id = %s;', (str(datasetId),))
        raw_result = cursor.fetchall()
        result = [
            Class(
                classId=item[0],
                datasetId=item[1],
                className=item[2]
            ) for item in raw_result
        ]
    return result


@router.get('/generatedImages')
def get_images(datasetId: int) -> list[GeneratedImage]:
    result: list[GeneratedImage] = []
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM generated_images WHERE dataset_id = %s;', (str(datasetId), ))
        raw_result = cursor.fetchall()
        result = [
            GeneratedImage(
                imageId=item[0],
                datasetId=item[1],
                imageData=bytes(item[2])
            ) for item in raw_result
        ] 
    return result


@router.get('/foregrounds')
def get_foregrounds(datasetId: int | None = None) -> list[ForegroundImage]:
    result: list[ForegroundImage] = []
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM foregrounds WHERE dataset_id = %s;', (str(datasetId), ))
        raw_result = cursor.fetchall()
        result = [
            ForegroundImage(
                foregroundId=item[0],
                datasetId=item[1],
                imageData=bytes(item[2])
            ) for item in raw_result
        ] 
    return result


@router.get('/backgrounds')
def get_backgrounds(datasetId: int | None = None) -> list[BackgroundImage]:
    result: list[BackgroundImage] = []
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM backgrounds WHERE dataset_id = %s;', (str(datasetId), ))
        raw_result = cursor.fetchall()
        result = [
            BackgroundImage(
                backgroundId=item[0],
                datasetId=item[1],
                imageData=bytes(item[2])
            ) for item in raw_result
        ] 
    return result


@router.get('/annotations')
def get_annotations(imageId: int) -> list[Annotation]:
    result: list[Annotation] = []
    with db_connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM annotations WHERE image_id = %s;', (str(imageId), )
        )
        raw_result = cursor.fetchall()
        result = [
            Annotation(
                annotationId=item[0],
                imageId=item[1],
                classId=item[2],
                centerX=item[3],
                centerY=item[4],
                normWidth=item[5],
                normHeight=item[6]
            ) for item in raw_result
        ]
    return result


@router.get('/generatedImagesGlob')
def get_images_glob(datasetId: int, pageSize: int, pageNumber: int) -> list[GeneratedImage]:
    result: list[GeneratedImage] = []
    with db_connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM generated_images WHERE dataset_id = %s',
            (str(datasetId),)
        )
        raw_result = cursor.fetchall()[pageNumber * pageSize : (pageNumber + 1) * pageSize]
        result = [
            GeneratedImage(
                imageId=item[0],
                datasetId=item[1],
                imageData=bytes(item[2])
            ) for item in raw_result
        ]
    return result