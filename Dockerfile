FROM python:3.11.6-slim-bookworm

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get install -y gcc


RUN pip install --upgrade pip 

COPY ./requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]