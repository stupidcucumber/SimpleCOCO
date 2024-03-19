import psycopg2
import pathlib
from psycopg2._psycopg import connection, cursor


def setup_database_connection(db_name: str, user: str, password: str, port: str, host: str, 
                              init_script: pathlib.Path) -> connection:
    result = psycopg2.connect(dbname=db_name, user=user, password=password, port=port, host=host)
    with result.cursor() as cursor:
        cursor.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname='public';")
        entries = cursor.fetchall()
        if len(entries) == 0:
            with init_script.open() as init_f:
                cursor.execute(init_f.read())
    result.commit()
    return result


def extract_images(dataset_id: int, cursor: cursor) -> list:
    cursor.execute(
        '''
        SELECT * FROM images WHERE dataset_id=%s;
        ''', (str(dataset_id),)
    )
    entries = [[*entry[:2], bytes(entry[2])] for entry in cursor.fetchall()]
    return entries