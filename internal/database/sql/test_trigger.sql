-- Класс эквивалентности №1
delete from postgres.public."user" u
where u.id = (select id
  from "user"
  where role != 'breeder'
  limit 1);

-- Класс эквивалентности №2
delete from postgres.public."user"
where role = 'breeder' and id = (select user_id
  from animal
  group by user_id
  having count(*) = 0
  limit 1);

-- Класс эквивалентности №3
delete from postgres.public."user" u
where u.id = (select user_id
  from animal
  where id in (select animal_id
    from animalshow
    where show_id in (select id
      from show
      where status = 'created'))
  group by user_id
  limit 1);

-- Класс эквивалентности №4
delete from postgres.public."user" u
where u.id = (select user_id
  from animal
  where id in (select animal_id
    from animalshow
    where show_id in (select id
      from show
      where status = 'started'))
  limit 1);