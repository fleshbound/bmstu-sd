COPY "user"(email, hashed_password, role, name) from '/tmp/user.csv' delimiter ';' csv header;
-- home/sheglar/bmstu/petowo/ppo/internal
COPY "group" (name) from '/tmp/group.csv' delimiter ';' csv header;

COPY Species (name, group_id) from '/tmp/species.csv' delimiter ';' csv header;

COPY Breed (name, species_id) from '/tmp/breed.csv' delimiter ';' csv header;

COPY animal(user_id, breed_id, name, birth_dt, sex, weight, height, length, has_defects, is_multicolor) from '/tmp/animal.csv' delimiter ';' csv header;

COPY Standard (breed_id, country, weight, height, length, has_defects, is_multicolor, weight_delta_percent,
               height_delta_percent, length_delta_percent) from '/tmp/standard.csv' delimiter ';' csv header;

COPY Show (species_id, breed_id, standard_id, status, country, show_class, name, is_multi_breed) from '/tmp/show.csv' delimiter ';' csv header;

COPY UserShow (show_id, user_id, is_archived) from '/tmp/usershow.csv' delimiter ';' csv header;

-- COPY Certificate (animalshow_id, rank)
--     from '/tmp/species.csv'
--     delimiter ';'
--     csv header;

COPY AnimalShow (show_id, animal_id, is_archived) from '/tmp/animalshow.csv' delimiter ';' csv header;

-- Score
