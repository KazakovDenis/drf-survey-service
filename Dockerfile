# cmd to build:
# docker build -t surveys:1.0 .
#
# cmd to run:
# docker run -d -p 8000:8000 --name surveys --env SURVEY_SECRET_KEY=$SURVEY_SECRET_KEY surveys:1.0
FROM python:3.8-alpine
LABEL maintainer="https://github.com/KazakovDenis"

# environment preparations
WORKDIR /www
COPY requirements.txt ./requirements.txt
RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# project preparations
COPY survey_service .
EXPOSE 8000
RUN python3 manage.py makemigrations && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collecstatic --noinput
CMD python3 manage.py runserver 0.0.0.0:8000
