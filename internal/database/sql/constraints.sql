create sequence user_id_seq owned by "user".id;
alter table "user"
    add primary key (id),
    alter column id set not null,
    alter column id set default nextval('user_id_seq'),
    alter column name set not null,
    alter column email set not null,
    alter column role set not null,
    alter column hashed_password set not null,
    add check (name != ''),
    add check (email != ''),
    add check (hashed_password != '');

create sequence group_id_seq owned by "group".id;
alter table "group"
    add primary key (id),
    alter column id set not null,
    alter column id set default nextval('group_id_seq'),
    alter column name set not null,
    add check (name != '');

create sequence species_id_seq owned by Species.id;
alter table Species
    add primary key (id),
    add foreign key (group_id) references "group"(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('species_id_seq'),
    alter column group_id set not null,
    alter column name set not null,
    add check (name != '');

create sequence breed_id_seq owned by Breed.id;
alter table Breed
    add primary key (id),
    add foreign key (species_id) references species(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('breed_id_seq'),
    alter column species_id set not null,
    alter column name set not null,
    add check (name != '');

create sequence animal_id_seq owned by Animal.id;
alter table Animal
    add primary key (id),
    add foreign key (user_id) references "user"(id),
    add foreign key (breed_id) references Breed(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('animal_id_seq'),
    alter column user_id set not null,
    alter column breed_id set not null,
    alter column name set not null,
    alter column birth_dt set not null,
    alter column sex set not null,
    alter column weight set not null,
    alter column height set not null,
    alter column length set not null,
    alter column has_defects set not null,
    alter column is_multicolor set not null,
    add check (name != ''),
    add check (weight > 0),
    add check (height > 0),
    add check (length > 0);

create sequence standard_id_seq owned by standard.id;
alter table standard
    add primary key (id),
    add foreign key (breed_id) references Breed(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('standard_id_seq'),
    alter column breed_id set not null,
    alter column country set not null,
    alter column weight set not null,
    alter column weight_delta_percent set not null,
    alter column height set not null,
    alter column height_delta_percent set not null,
    alter column length set not null,
    alter column length_delta_percent set not null,
    alter column has_defects set not null,
    alter column is_multicolor set not null,
    add check (weight_delta_percent > 0),
    add check (weight > 0),
    add check (height_delta_percent > 0),
    add check (height > 0),
    add check (length_delta_percent > 0),
    add check (length > 0);

create sequence show_id_seq owned by Show.id;
alter table Show
    add primary key (id),
    add foreign key (species_id) references Species(id) on delete cascade,
    add foreign key (breed_id) references Breed(id) on delete cascade,
    add foreign key (standard_id) references Standard(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('show_id_seq'),
    alter column country set not null,
    alter column name set not null,
    alter column status set not null,
    alter column show_class set not null,
    alter column is_multi_breed set not null,
    add check (name != ''),
    add check (show_class != '');

create sequence usershow_id_seq owned by UserShow.id;
alter table UserShow
    add primary key (id),
    add foreign key (user_id) references "user"(id) on delete cascade,
    add foreign key (show_id) references Show(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('usershow_id_seq'),
    alter column user_id set not null,
    alter column show_id set not null,
    alter column is_archived set not null;

create sequence animalshow_id_seq owned by AnimalShow.id;
alter table AnimalShow
    add primary key (id),
    add foreign key (show_id) references Show(id) on delete cascade,
    add foreign key (animal_id) references Animal(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('animalshow_id_seq'),
    alter column animal_id set not null,
    alter column show_id set not null,
    alter column is_archived set not null;

create sequence certificate_id_seq owned by certificate.id;
alter table certificate
    add primary key (id),
    add foreign key (animalshow_id) references AnimalShow(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('certificate_id_seq'),
    alter column animalshow_id set not null,
    alter column rank set not null;

create sequence score_id_seq owned by score.id;
alter table score
    add primary key (id),
    add foreign key (animalshow_id) references AnimalShow(id) on delete cascade,
    add foreign key (usershow_id) references UserShow(id) on delete cascade,
    alter column id set not null,
    alter column id set default nextval('score_id_seq'),
    alter column animalshow_id set not null,
    alter column usershow_id set not null,
    alter column value set not null,
    alter column is_archived set not null,
    alter column dt_created set not null,
    add check (value >= 0);
