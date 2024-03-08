### 1. Название проекта

Выставочное агенство "Выставлятор" (организация выставок различных видов животных)

### 2. Краткое описание идеи проекта

Приложение, имитирующее работу выставочного агенства. Приложение должно предоставлять функционал для хозяев, экспертов, организаторов.

### 3. Краткое описание предметной области

Понятия: выставка, вид, порода, эксперт, организатор, оценка.

Выставка животных некоторого вида --- публичное мероприятие по оценке степени соответствия участвующих в выставке животных заданным для породы или вида стандартам [[1]](https://elibrary.ru/item.asp?id=48512966), [[2]](https://elibrary.ru/item.asp?id=41275973). Для регистрации животного на выставку заводчику, который является его хозяином, необходимо заполнить электронную анкету с информацией об участнике [[1]](https://elibrary.ru/item.asp?id=41275973). Оценку животных проводят приглашенные на выставку судьи. /Для того, чтобы быть приглашенным на выставку, судье необходимо иметь допустимые для судейства этой выставки свойства (звание, стаж, количество выставок) [[3]](https://rkf.org.ru/wp-content/uploads/2019/11/polozhenie-o-sudjah-rkf-fci-s-01.01.2020.pdf)./ После завершения выставки каждый участник выставки получает диплом об участии, содержащий информацию о занятом месте, полученных оценках, титуле, минимальную информацию о выставке. Созданием выставки управляет организатор выставки --- ответственное лицо, назначенное некоторой организацией. В рамках работы считается, что организация --- единственная.

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
Все рассмотренные возможности реализуются в данном проекте.

### 6. Краткое описание акторов (ролей)

1. Хозяин: зарегистрированный пользователь, который владеет 0 или более животными различных видов, может управлять записями о своих животных, регистрировать их на выставки (одно животное может участвовать в нескольких выставках).
2. Судья (эксперт): зарегистрированный пользователь, который может оценивать участников выставки, если является приглашенным судьей.
3. Организатор: зарегистрированный пользователь, который управляет всеми выставками (создание, удаление, редактирование общей информации, управление списком участников, приглашенных судей).
4. Гость: может посмотреть список выставок, результаты выставки.

### 7. Use-Case - диаграмма

![usecase.png](./img/usecase.png)

### 8. ER-диаграмма сущностей

![erdiagram.png](./img/erdiagram.png)

#### Диаграмма состояний

### 9. Пользовательские сценарии

```
1) ПРОСМОТР ВЫСТАВОК
1.1) Пользователь входит как Гость/Заводчик/Эксперт/Организатор
1.2) Гость/Заводчик/Эксперт/Организатор смотрит список выставок
2) ДОБАВЛЕНИЕ ЖИВОТНОГО
2.1) Пользователь входит как Заводчик
2.2) Заводчик добавляет животное
3) СОЗДАНИЕ ВЫСТАВКИ
3.1) Пользователь входит как Организатор
3.2) Организатор создает выставку
```

#### Сложные сценарии

```
4) УДАЛЕНИЕ ЭКСПЕРТА
4.1) Пользователь входит как Организатор
4.2) Организатор выбирает выставку
4.3) Организатор хочет удалить эксперта
4.4) Прервать действие, если выставка является завершенной или запущенной
4.5) Прервать действие, если на выставке нет приглашенных экспертов
4.6) Организатор выбрал эксперта
4.7) Удалить эксперта с выставки
5) ДОБАВЛЕНИЕ ЭКСПЕРТА
5.1) Пользователь входит как Организатор
5.2) Организатор выбирает выставку
5.3) Организатор хочет добавить эксперта на выставку
5.4) Прервать действие, если выставка является завершенной или запущенной
5.5) Прервать действие, если эксперт уже приглашен на выбранную выставку
5.6) Добавить эксперта на выставку (пометить его как приглашенного)
6) РЕДАКТИРОВАНИЕ ВЫСТАВКИ
6.1) Пользователь входит в систему как Организатор
6.2) Организатор выбирает выставку
6.3) Организатор хочет редактировать информацию о выставке
6.4) Прервать действие, если выставка является запущенной или завершенной
6.5) Редактировать информацию о выставке
6) ЗАПУСК ВЫСТАВКИ
6.1) Пользователь входит в систему как Организатор
6.2) Пользователь выбирает выставку
6.3) Организатор хочет запустить выставку
6.4) Прервать действие, если выставка является завершенной
6.5) Прервать действие, если на выставке менее 3 участников
6.6) Прервать действие, если нет приглашенных экспертов
6.7) Отметить выставку запущенной
7. ЗАВЕРШЕНИЕ ВЫСТАВКИ
7.1) Пользователь входит в систему как Организатор
7.2) Организатор выбирает выставку
7.3) Организатор хочет завершить выставку
7.4) Прервать действие, если выставка не является запущенной
7.5) Прервать действие, если есть хотя бы один эксперт, не оценивший всех участников
7.6) Отметить выставку завершенной
7.7) Вычислить результаты выставки
8. УДАЛЕНИЕ ЖИВОТНОГО
8.1) Пользователь входит в систему как Заводчик
8.2) Заводчик хочет удалить животное
8.3) Прервать действие, если у него нет животных
8.4) Заводчик выбирает животное
8.5) Прервать действие, если животное является участником хотя бы одной запущенной выставки
8.6) Отметить данные о результатах завершенных выставок, в которых участвовало животное, как архивные
8.7) Удалить животное из системы
9. ЗАПИСЬ ЖИВОТНОГО НА ВЫСТАВКУ
9.1) Пользователь входит в в систему как Заводчик
9.2) Заводчик хочет записать животных на выставку
9.3) Прервать действие, если нет животных
9.4) Прервать действие, если нет животных, подходящих по виду и/или породе
9.5) Заводчик выбирает животное
9.6) Прервать действие, если выбранное животное уже записано на выставку
9.7) Записать животное на выставку
10) ПРОСМОТР РЕЗУЛЬТАТОВ ВЫСТАВКИ
10.1) Пользователь входит как Гость/Заводчик/Эксперт/Организатор
10.2) Пользователь выбирает выставку
10.3) Пользователь хочет посмотреть результаты выставки
10.4) Прервать действие, если выставка не является завершенной
10.5) Сформировать отчет о результатах выставки
10.6) Предоставить отчет пользователю
```

### 10. Формализация ключевых бизнес-процессов

Диаграмма процесса входа в систему и выполнения начальных действий

![bpmn_enter.png](./img/bpmn_enter.png)
