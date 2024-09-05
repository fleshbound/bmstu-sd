create table if not exists Animal (
    id int,
    user_id int,
    breed_id int,
    "name" text,
    birth_dt date,
    sex text,
    weight float,
    height float,
    "length" float,
    has_defects bool,
    is_multicolor bool
);

create table if not exists "user" (
    id int,
    email text,
    hashed_password text,
    "role" text,
    "name" text
);

create table if not exists UserShow (
    id int,
    show_id int,
    user_id int,
    is_archived bool
);

create table if not exists AnimalShow (
    id int,
    show_id int,
    animal_id int,
    is_archived bool
);

create table if not exists Standard (
    id int,
    breed_id int,
    country text,
    weight float,
    height float,
    length float,
    has_defects bool,
    is_multicolor bool,
    weight_delta_percent float,
    height_delta_percent float,
    length_delta_percent float
);

create table if not exists Species (
    id int,
    name text,
    group_id int
);

create table if not exists Breed (
    id int,
    name text,
    species_id int
);

create table if not exists "group" (
    id int,
    name text
);

create table if not exists Score (
    id int,
    usershow_id int,
    animalshow_id int,
    value int,
    is_archived bool
);

create table if not exists Certificate (
    id int,
    animalshow_id int,
    rank int
);

create table if not exists Show (
    id int,
    species_id int,
    breed_id int,
    standard_id int,
    status text,
    country text,
    show_class text,
    name text,
    is_multi_breed bool
);
