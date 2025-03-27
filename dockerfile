FROM python:3.12-slim 

WORKDIR /app

COPY . /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput


CMD [ "gunicorn", "--bind", "0.0.0:8000", "360SolveHRMS.wsgi.application" ]
