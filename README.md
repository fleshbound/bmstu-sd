### Название проекта

Разработка базы данных для хранения и обработки данных агенства организации выставки животных различных видов.

### Краткое описание идеи проекта

Имеются выставки, в которых участвуют животные различных видов, у которых имеются хозяева. За создание и управление выставками отвечают назначенные ответственные лица. Оценку животных проводят приглашенные на выставку судьи, а за участие в выставке животное получает диплом об участии, в котором содержится информация о результатах.

### Краткое описание предметной области

Выставка животных некоторого вида --- публичное мероприятие по оценке степени соответствия участвующих в выставке животных заданным для породы рассматриваемого вида стандартам [[1]](https://elibrary.ru/item.asp?id=48512966), [[2]](https://elibrary.ru/item.asp?id=41275973). Для регистрации животного на выставку хозяину необходимо заполнить электронную анкету с информацией об участнике [[1]](https://elibrary.ru/item.asp?id=41275973). Оценку животных проводят приглашенные на выставку судьи. Для того, чтобы быть приглашенным на выставку, судье необходимо иметь допустимые для судейства этой выставки свойства (звание, стаж, количество выставок) [[3]](https://rkf.org.ru/wp-content/uploads/2019/11/polozhenie-o-sudjah-rkf-fci-s-01.01.2020.pdf). После завершения выставки каждый участник выставки получает диплом об участии, содержащий информацию о занятом месте, полученных оценках, титуле, минимальную информацию о выставке. Созданием выставки управляет организатор выставки --- ответственное лицо, назначенное некоторой организацией. В рамках работы считается, что организация --- единственная, организатор выставки --- единственный.

### Краткий анализ аналогичных решений

Критерии:

1. Наличие возможности регистрации животных разных видов.
2. Наличие возможности проведения всех этапов выставки в онлайн-формате.
3. Наличие возможности автоматической обработки результатов оценки участников.

|   | 1 | 2 | 3 |
|---|---|---|---|
| https://cats-show.org | - | + | - |
| https://brd-show.online | - | + | + |
| https://www.show-dogs.ru | - | - | - |
| https://dog-planeta.ru | - | - | - |
| Онлайн-выставка "Мой питомец" с использованием ВКонтакте | + | + | - |

### Краткое обоснование целесообразности и актуальности проекта

В 21 веке вследствие увеличения доступности информации появляется все больше людей, увлекающихся разведением домашних животных, относящихся к видам, которые распространены меньше, чем кошки и собаки, а также разводящих несколько видов одновременно, поэтому целесообразно создание проекта, который объединяет организацию выставок для различных видов животных. Работа над данным проектом является актуальной, так как перевод выставок в онлайн-формат с автоматической обработкой результатов упрощает работу судей, уменьшает трудозатраты на обработку результатов и распределение наград, снижает риск возникновения ошибок обработки.

### Краткое описание акторов (ролей)

1. Хозяин: владеет 0 или более животными различных видов, может управлять записями о своих животных, регистрировать их на выставки (одно животное может участвовать в нескольких выставках).
2. Судья: может оценивать участников выставки, если является приглашенным судьей.
3. Организатор: управляет всеми выставками (создание, удаление, редактирование общей информации, управление списком участников, приглашенных судей).

### Use-Case - диаграмма



### ER-диаграмма сущностей



### Пользовательские сценарии



### Формализация ключевых бизнес-процессов


