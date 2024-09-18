create or replace function user_safe_delete()
returns trigger
as
$$
declare
    animal_count integer;
    started_show_count integer;
begin
    if old.role != 'breeder' then
        return old;
    end if;

    drop table if exists animal_ids;

    create temp table animal_ids as
    select a.id
    from postgres.public.animal as a
    where a.user_id = old.id;

    select count(*)
        into animal_count
    from animal_ids;

    if animal_count = 0 then
        raise notice 'user has no animals, deleting...';
        return old;
    end if;

    select count(*)
    into started_show_count
    from postgres.public.show as s
    where s.status = 'started' and s.id in (select ash.show_id
                                            from postgres.public.animalshow as ash
                                            where ash.animal_id in (select * from animal_ids));

    if started_show_count > 0 then
        RAISE exception 'cannot delete user with animals at started shows';
    else
        delete from animal
        where user_id = old.id;

        return old;
    end if;
end;$$ language plpgsql;

drop trigger if exists user_delete on postgres.public."user";

create trigger user_delete
before delete on postgres.public."user"
for each row
execute procedure user_safe_delete();
