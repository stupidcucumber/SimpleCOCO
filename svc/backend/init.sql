CREATE TABLE datasets (
    dataset_id SERIAL PRIMARY KEY,
    dataset_name VARCHAR(255),
    dataset_description TEXT
);

CREATE TABLE classes (
    class_id SERIAL PRIMARY KEY,
    dataset_id INT,
    class_name VARCHAR(50),
    CONSTRAINT fk_dataset
        FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE generated_images (
    image_id SERIAL PRIMARY KEY,
    dataset_id INT,
    image_data bytea,
    CONSTRAINT fk_dataset
        FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE backgrounds (
    background_id SERIAL PRIMARY KEY,
    dataset_id INT,
    image_data bytea,
    CONSTRAINT fk_dataset
        FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id)
);

CREATE TABLE foregrounds (
    foreground_id SERIAL PRIMARY KEY,
    dataset_id INT,
    class_id INT,
    image_data bytea,
    mask_data bytea,
    CONSTRAINT fk_dataset
        FOREIGN KEY(dataset_id) REFERENCES datasets(dataset_id),
    CONSTRAINT fk_class
        FOREIGN KEY(class_id) REFERENCES classes(class_id)
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
        FOREIGN KEY(image_id) REFERENCES generated_images(image_id),
    CONSTRAINT fk_class
        FOREIGN KEY(class_id) REFERENCES classes(class_id)
);