# Руководство использованию по API
В данном руководстве приведены минимально рабочие примеры.

Принятые определения:  
Схема (scheme) - документ, созданный администратором и содержащий информацию об опросе.  
Опрос (survey) - документ, просматриваемый и заполняемый участником опроса.  

Переменная SURVEY_ADDR - адрес, на котором развернут сервис (по умолчанию *http://localhost:8000*).

## Функционал администратора
### Аутентификация в сервисе  

- по логину и паролю
```
curl -X GET $SURVEY_ADDR/api/v1/schemes/ -u user:password 
```
- по токену
```
curl -X GET $SURVEY_ADDR/api/v1/schemes/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```
Для получения токена выполнить запрос:
```
curl -X POST $SURVEY_ADDR/api/auth/get-token/  -H "Content-Type: application/json" -d 
'{
    "username": "имя_пользователя", 
    "password": "пароль"
}'
```

### Получение списка схем
```
curl -X GET $SURVEY_ADDR/api/v1/schemes/
```
  
### Создание схемы
```
curl -X POST $SURVEY_ADDR/api/v1/schemes/ -d 
'{
    "name": "Первый опрос",
    "date_from": "2020-12-01",
    "date_to": "2020-12-15"
}'
```
Необязательные поля: description, questions.
    
### Получение полной информации о схеме
```
curl -X GET $SURVEY_ADDR/api/v1/schemes/<uuid:id схемы>
```
  
### Изменение схемы
```
curl -X PATCH $SURVEY_ADDR/api/v1/schemes/<uuid:id схемы> -d
'{
    "description": "Описание первого опроса"
}'
```
    
### Удаление схемы
```
curl -X DELETE $SURVEY_ADDR/api/v1/schemes/<uuid:id схемы>
```   
 
### Добавление вопроса в схему
```
curl -X PATCH $SURVEY_ADDR/api/v1/schemes/<uuid:id схемы> -d
'{
    "questions": [
        {
            "text": "Первый вопрос",
            "answer_type": "TEXT"
        }
    ]
}'
```
Новый вопрос будет создан, если не указан его "id".  
Варианты "answer_type": TEXT, SINGLE, MULTIPLE.  
При указании SINGLE и MULTIPLE необходимо передать в дополнительном поле "answer_options" список возможных ответов.  
      
### Изменение вопроса
```
curl -X PATCH $SURVEY_ADDR/api/v1/schemes/<uuid:id схемы> -d 
'{
    "questions": [
        {
            "id": "uuid вопроса"
            "answer_type": "SINGLE",
            "answer_options": [
                "Первый вариант ответа",
                "Второй вариант ответа"
            ]
        }
    ]
}'
```
Передать "id" вопроса и изменяемые поля.
    
### Удаление вопроса
```
curl -X PATCH $SURVEY_ADDR/api/v1/schemes/<uuid:id схемы> -d
'{
    "questions": [
        {"id": "uuid вопроса"}
    ]
}'
```
Будут удалены все вопросы, у которых передан только "id".    

### Получение списка участников опросов
```
curl -X GET $SURVEY_ADDR/api/v1/participants/
```

### Получение информации об участнике и пройденных им опросах
```
curl -X GET $SURVEY_ADDR/api/v1/participants/<int:id участника>
``` 
  
## Функционал участника опроса
### Получение списка активных опросов
```
curl -X GET $SURVEY_ADDR/api/v1/surveys/
```

### Прохождение опроса анонимно
```
curl -X GET $SURVEY_ADDR/api/v1/scheme/<uuid:id схемы>/take
```
URL для прохождения опросов получают из списка опросов.

### Прохождение опроса участником, уже проходившим опросы
```
curl -X GET $SURVEY_ADDR/api/v1/scheme/<uuid:id схемы>/take?participant_id=<int:id участника>    
```
"participant_id" получают из первого опроса, пройденного анонимно.
  
### Отправка ответов
```
curl -X PATCH $SURVEY_ADDR/api/v1/surveys/<uuid:id опроса> -d
'{
    "answers": [
            {
                "id": "uuid ответа"
                "answer": [
                    "Первый вариант ответа",
                    "Второй вариант ответа",
                ]
            }
        ]
}'
```  
Приведён пример для answer_type=MULTIPLE. Для TEXT и SINGLE передаётся строка.
           
### Просмотр результатов опроса
```
curl -X GET $SURVEY_ADDR/api/v1/surveys/<uuid:id опроса>
```  
   
### Получение информации об участнике и пройденных им опросах
```
curl -X GET $SURVEY_ADDR/api/v1/participants/<int:id участника>
```
     