```
GET     /show - получить список всех выставок
POST    /show - создать выставку
GET     /show/{show_id}/result - получить результаты выставки
GET     /show/{show_id}/animals - получить список участников выставки
POST    /show/{show_id}/stop - завершить выставку
POST    /show/{show_id}/start - запустить выставку
POST    /show/{show_id}/animals/{animal_id}/register - записать животное на выставку
POST    /show/{show_id}/animals/{animal_id}/unregister - отписать животное от выставки
```

```
POST    /score - оценить участника
```

```
GET     /animal
POST    /animal - создать животное
GET     /animal/{animal_id}
DELETE  /animal/{animal_id}
GET     /animal/user/{user_id}
```

```
POST    /user/{user_id}/register/{show_id} - добавить судью на выставку
POST    /user/{user_id}/unregister/{show_id} - удалить судью с выставки
```

```
POST    /login - войти
POST    /logout - выйти
```