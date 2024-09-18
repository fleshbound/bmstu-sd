drop sequence if exists user_id_seq, animal_id_seq, usershow_id_seq, animalshow_id_seq,
    show_id_seq, score_id_seq, certificate_id_seq, standard_id_seq, species_id_seq,
    group_id_seq, breed_id_seq cascade;
drop table if exists Animal cascade;
drop table if exists "user" cascade;
drop table if exists UserShow cascade;
drop table if exists AnimalShow cascade;
drop table if exists Show cascade;
drop table if exists Score cascade;
drop table if exists Certificate cascade;
drop table if exists Standard cascade;
drop table if exists Species cascade;
drop table if exists "group" cascade;
drop table if exists Breed cascade;

drop type if exists country;
drop type if exists show_status;
drop type if exists sex;
drop type if exists user_role;


