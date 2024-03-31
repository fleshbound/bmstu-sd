/*

POST    /login
POST    /logout

GET     /users                                        получить список пользователей
GET     /users/{user_id}/animals                      получить список животных
POST    /users/{user_id}/animals                      создать животное
DELETE  /users/{user_id}/animals/{animal_id}          удалить животное

GET     /shows                                        получить список выставок
GET     /shows/{show_id}                              получить информацию о выставке
GET     /shows/{show_id}/results                      получить результаты выставки
GET     /shows/{show_id}/animals                      получить всех участников
POST    /shows/{show_id}/animals                      добавить участника
GET     /shows/{show_id}/animals/{animal_id}          получить участника
POST    /shows/{show_id}/animals/{animal_id}/scores   поставить оценку участнику
PUT     /shows/{show_id}/animals/{animal_id}/scores/{score_id}        отметить выставку архивированной
POST    /shows/{show_id}/users                        добавить судью
DELETE  /shows/{show_id}/users/{user_id}              удалить судью

*/ 

@main def hello(): Unit =
  println("Hello world!")
  println(msg)
  println(tst)

def msg = "I was compiled by Scala 3. :)"

val tst = List[String]()
