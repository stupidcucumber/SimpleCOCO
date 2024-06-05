from fastapi import APIRouter
from psycopg2._psycopg import connection
from ..structs import (
    Class,
    Dataset,
    GeneratedImage,
    Annotation,
    ForegroundImage,
    BackgroundImage
)

router = APIRouter(
    prefix='/fill'
)
db_connection = None
def set_connection(_connection: connection) -> None:
    global db_connection
    db_connection = _connection


@router.post('/dataset')
def post_dataset(dataset: Dataset) -> Dataset:
    with db_connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO datasets (dataset_name, dataset_description) VALUES (%s, %s);', 
            (dataset.datasetName, dataset.datasetDescription)
        )
        item_id = cursor.lastrowid
        dataset.datasetId = item_id
    db_connection.commit()
    return dataset


@router.post('/class')
def post_class(new_class: Class) -> list[Class]:
    with db_connection.cursor() as cursor:
        cursor.execute(
            '''
                INSERT INTO classes (dataset_id, class_name) VALUES (%s, %s);
            ''',
            (str(new_class.datasetId), new_class.className)
        )
        item_id = cursor.lastrowid
        new_class.classId = item_id
    db_connection.commit()
    return new_class


@router.post('/generatedImage')
def post_generated_image(generatedImage: GeneratedImage):
    with db_connection.cursor() as cursor:
        cursor.execute(
            '''
            INSERT INTO generated_images (dataset_id, image_data) VALUES (%s, %s);
            ''', 
            (
                str(generatedImage.datasetId), 
                generatedImage.imageData.encode()
            )
        )
    db_connection.commit()
    return 200


@router.post('/foregroundImage')
def post_foreground_image(foregroundImage: ForegroundImage):
    with db_connection.cursor() as cursor:
        cursor.execute(
            '''
            INSERT INTO generated_images (dataset_id, image_data) VALUES (%s, %s);
            ''', 
            (
                str(foregroundImage.datasetId), 
                foregroundImage.imageData.encode()
            )
        )
    db_connection.commit()
    return 200


@router.post('/backgroundImage')
def post_background_image(backgroundImage: BackgroundImage):
    with db_connection.cursor() as cursor:
        cursor.execute(
            '''
            INSERT INTO generated_images (dataset_id, image_data) VALUES (%s, %s);
            ''', 
            (
                str(backgroundImage.datasetId), 
                backgroundImage.imageData.encode()
            )
        )
    db_connection.commit()
    return 200


@router.post('/annotation')
def post_annotation(annotation: Annotation) -> Annotation:
    with db_connection.cursor() as cursor:
        cursor.execute(
            '''
                INSERT INTO annotations (
                    image_id,
                    class_id,
                    center_x,
                    center_y,
                    norm_width,
                    norm_height
                ) VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (
                str(annotation.imageId), str(annotation.classId), str(annotation.centerX),
                str(annotation.centerY), str(annotation.normWidth), str(annotation.normHeight)
            )
        )
        item_id = cursor.lastrowid
        annotation.annotationId = item_id
    return annotation