FROM python:3.11-alpine

ENV APP \Project_informator

WORKDIR $APP

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]