import pathlib, os
from fastapi import FastAPI
from src.utils.database import setup_database_connection


db_connection = setup_database_connection(
    db_name=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    port=os.environ['POSTGRES_PORT'],
    host=os.environ['POSTGRES_HOST'],
    init_script=pathlib.Path('init.sql')
)

app = FastAPI()

@app.get('/')
def check_health():
    return 'Working'