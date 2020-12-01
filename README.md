# API бекенда для системы опросов
[Техническое задание](https://github.com/KazakovDenis/fabrique_studio/blob/main/task.txt)  

## Использованный технологический стек
* Django 2.2.10
* Django REST framework 3.12.2
* Docker

## Документация
[Руководство по использованию данного API](https://github.com/KazakovDenis/fabrique_studio/blob/main/survey_service/api/v1/docs/docs.md)  
  
OpenAPI-спецификация доступна по URL:  */api/v1/doc*  

## Запуск сервиса
* Для запуска в docker-контейнере необходимо:  

    * создать образ
    ```
    docker build -t surveys:1.0 . 
    ```
    * запустить контейнер  
    ```
    docker run -d \
         -p 8000:8000 \
         --name surveys \
         surveys:1.0 \
    ```
 