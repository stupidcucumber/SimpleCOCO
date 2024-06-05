from pydantic import BaseModel


class Annotation(BaseModel):
    '''
    CREATE TABLE annotations (
        annotation_id SERIAL PRIMARY KEY,
        image_id INT,
        class_id INT,
        center_x NUMERIC(5),
        center_y NUMERIC(5),
        norm_width NUMERIC(5),
        norm_height NUMERIC(5),
        CONSTRAINT fk_image
            FOREIGN KEY(image_id) REFERENCES images(image_id),
        CONSTRAINT fk_class
            FOREIGN KEY(class_id) REFERENCES classes(class_id)
    );
    '''
    annotationId: int | None = None
    imageId: int
    classId: int
    centerX: float
    centerY: float
    normWidth: float
    normHeight: float