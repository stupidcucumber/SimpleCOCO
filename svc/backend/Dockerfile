FROM python:3.10-bullseye

WORKDIR /app
ADD requirements.txt /app/

RUN pip install -r requirements.txt
COPY . /app/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]