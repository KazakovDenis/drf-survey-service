# cmd to build:
# docker build -t surveys:1.0 \
#   --build-arg DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL \
#   --build-arg DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME \
#   --build-arg DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD .
#
# cmd to run:
# docker run -d -p 8000:8000 --name surveys surveys:1.0
FROM python:3.8-alpine
LABEL maintainer="https://github.com/KazakovDenis"

# environment preparations
WORKDIR /www
COPY requirements.txt ./requirements.txt
RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
ARG DJANGO_SUPERUSER_EMAIL
ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_PASSWORD

# project preparations
COPY survey_service .
EXPOSE 8000
RUN python3 manage.py makemigrations && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collecstatic --noinput && \
    python3 manage.py createsuperuser --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
CMD python3 manage.py runserver 0.0.0.0:8000
