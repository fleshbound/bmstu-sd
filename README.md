### 1. Название проекта

"Выставлятор"

### 2. Краткое описание идеи проекта

Приложение, имитирующее работу выставочного агенства. Приложение должно предоставлять функционал для хозяев, экспертов и организатора. 

### 3. Краткое описание предметной области

Выставка животных некоторого вида --- публичное мероприятие по оценке степени соответствия участвующих в выставке животных заданным для породы или вида стандартам [[1]](https://elibrary.ru/item.asp?id=48512966), [[2]](https://elibrary.ru/item.asp?id=41275973). Для регистрации животного на выставку заводчику, который является его хозяином, необходимо заполнить электронную анкету с информацией об участнике [[1]](https://elibrary.ru/item.asp?id=41275973). Оценку животных проводят приглашенные на выставку судьи. /Для того, чтобы быть приглашенным на выставку, судье необходимо иметь допустимые для судейства этой выставки свойства (звание, стаж, количество выставок) [[3]](https://rkf.org.ru/wp-content/uploads/2019/11/polozhenie-o-sudjah-rkf-fci-s-01.01.2020.pdf)./ После завершения выставки каждый участник выставки получает диплом об участии, содержащий информацию о занятом месте, полученных оценках, титуле, минимальную информацию о выставке. Созданием выставки управляет организатор выставки --- ответственное лицо, назначенное некоторой организацией. В рамках работы считается, что организация --- единственная, организатор выставки --- единственный.

### 4. Краткий анализ аналогичных решений

Критерии:

1. Наличие возможности регистрации животных разных видов.
2. Наличие возможности проведения всех этапов выставки в онлайн-формате.
3. Наличие возможности автоматической обработки результатов оценки участников.

|   | 1 | 2 | 3 |
|---|---|---|---|
| cats-show.org | - | + | - |
| brd-show.online | - | + | + |
| www.show-dogs.ru | - | - | - |
| dog-planeta.ru | - | - | - |
| Онлайн-выставка "Мой питомец" с использованием ВКонтакте | + | + | - |
| Предлагаемое решение | + | + | + |

### 5. Краткое обоснование целесообразности и актуальности проекта

В 21 веке вследствие увеличения доступности информации появляется все больше людей, увлекающихся разведением домашних животных, относящихся к видам, которые распространены меньше, чем кошки и собаки, а также разводящих несколько видов одновременно, поэтому целесообразно создание проекта, который объединяет организацию выставок для различных видов животных. Работа над данным проектом является актуальной, так как перевод выставок в онлайн-формат с автоматической обработкой результатов
- упрощает работу судей,
- уменьшает трудозатраты на обработку результатов и распределение наград,
- снижает риск возникновения ошибок обработки.

### 6. Краткое описание акторов (ролей)

1. Хозяин: зарегистрированный пользователь, который владеет 0 или более животными различных видов, может управлять записями о своих животных, регистрировать их на выставки (одно животное может участвовать в нескольких выставках).
2. Судья (эксперт): зарегистрированный пользователь, который может оценивать участников выставки, если является приглашенным судьей.
3. Организатор: зарегистрированный пользователь, который управляет всеми выставками (создание, удаление, редактирование общей информации, управление списком участников, приглашенных судей).
4. Гость: может зарегистрироваться, посмотреть список выставок.
5. Зарегистрированный пользователь: может войти в систему, выйти из системы, посмотреть список выставок.

### 7. Use-Case - диаграмма

![usecase.png](./img/usecase.png)

### 8. ER-диаграмма сущностей

![erdiagram.png](./img/erdiagram.png)

### 9. Пользовательские сценарии

```
1)
1.1) Пользователь заходит в систему как Гость
1.2) Гость смотрит список выставок
2)
2.1) Пользователь заходит в систему как Гость
2.2) Гость регистрируется
3)
3.1) Пользователь заходит в систему как Гость
3.2) Гость вводит пароль, логин и входит как Заводчик
3.3) Заводчик добавляет животное
4)
4.1) Пользователь заходит в систему как Зарегистрированный пользователь
4.2) Зарегистрированный пользователь вводит пароль, логин и входит как Заводчик
4.3) Заводчик выбирает животное
4.4) Заводчик удаляет выбранное животное
5)
5.1) Пользователь заходит в систему как Зарегистрированный пользователь
5.2) Зарегистрированный пользователь вводит пароль, логин и входит как Заводчик
5.3) Заводчик выбирает животное
5.4) Заводчик редактирует животное (информацию о нем)
6)
6.1) Пользователь заходит в систему как Зарегистрированный пользователь
6.2) Зарегистрированный пользователь вводит пароль, логин и входит как Заводчик
6.3) Заводчик смотрит список выставок
7)
7.1) Пользователь заходит в систему как Зарегистрированный пользователь
7.2) Зарегистрированный пользователь вводит пароль, логин и входит как Заводчик
7.3) Заводчик выбирает животное
7.4) Заводчик выбирает выставку
7.5) Заводчик записывает выбранное животное на выбранную выставку/отписывает животное от выбранной выставки
8)
8.1) Пользователь заходит в систему как Зарегистрированный пользователь
8.2) Зарегистрированный пользователь вводит пароль, логин и входит как Эксперт
8.3) Эксперт выбирает запущенную выставку из тех, на которые он приглашен
8.4) Эксперт выбирает участника выбранной выставки
8.5) Эксперт ставит оценку выбранному участнику
9)
9.1) Пользователь заходит в систему как Зарегистрированный пользователь
9.2) Зарегистрированный пользователь вводит пароль, логин и входит как Эксперт
9.3) Организатор создает выставку
10)
10.1) Пользователь заходит в систему как Зарегистрированный пользователь
10.2) Зарегистрированный пользователь вводит пароль, логин и входит как Организатор
10.3) Организатор выбирает выставку
10.4) Организатор редактирует информацию о выбранной выставке/запускает выбранную выставку/завершает выбранную выставку
11)
11.1) Пользователь заходит в систему как Зарегистрированный пользователь
11.2) Зарегистрированный пользователь вводит пароль, логин и входит как Организатор
11.3) Организатор выбирает выставку
11.4) Организатор выбирает эксперта
11.5) Организатор добавляет выбранного эксперта на выставку
12)
12.1) Пользователь заходит в систему как Зарегистрированный пользователь
12.2) Зарегистрированный пользователь вводит пароль, логин и входит как Организатор
12.3) Организатор выбирает выставку
12.4) Организатор выбирает эксперта
12.5) Организатор удаляет выбранного эксперта с выставки
```

### 10. Формализация ключевых бизнес-процессов


