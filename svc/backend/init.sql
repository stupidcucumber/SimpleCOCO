CREATE TABLE classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(50)
);

CREATE TABLE datasets (
    dataset_id SERIAL PRIMARY KEY,
    dataset_name VARCHAR(255)
);

CREATE TABLE images (
    image_id SERIAL PRIMARY KEY,
    dataset_id INT,
    image_data bytea,
    CONSTRAINT fk_dataset
        FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

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