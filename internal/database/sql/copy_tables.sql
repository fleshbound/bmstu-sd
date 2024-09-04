copy animal(id, user_id, breed_id, name, birth_dt, sex, weight, height, length, has_defects, is_multicolor)
from '/home/sheglar/bmstu/db/lab_01/data/animal.csv'
delimiter ';'
header csv;

copy "User"(email, hashed_password, role, name)
from '/home/sheglar/bmstu/db/lab_01/data/user.csv'
delimiter ';'
header csv;

copy UserShow (show_id, user_id, is_archived)
from '/home/sheglar/bmstu/db/lab_01/data/usershow.csv'
delimiter ';'
header csv;

copy AnimalShow (show_id, animal_id, is_archived)
from '/home/sheglar/bmstu/db/lab_01/data/animalshow.csv'
delimiter ';'
header csv;

copy Standard (breed_id, country, weight, height, length, has_defects, is_multicolor, weight_delta_percent,
               height_delta_percent, length_delta_percent)
from '/home/sheglar/bmstu/db/lab_01/data/standard.csv'
delimiter ';'
header csv;

copy Species (name, group_id)
from '/home/sheglar/bmstu/db/lab_01/data/species.csv'
delimiter ';'
header csv;

copy "Group" (name)
from '/home/sheglar/bmstu/db/lab_01/data/group.csv'
delimiter ';'
header csv;

copy Breed (name, species_id)
from '/home/sheglar/bmstu/db/lab_01/data/breed.csv'
delimiter ';'
header csv;

copy Certificate (animalshow_id, rank)
from '/home/sheglar/bmstu/db/lab_01/data/species.csv'
delimiter ';'
header csv;

copy Show (species_id, breed_id, standard_id, status, country, show_class, name, is_multi_breed)
from '/home/sheglar/bmstu/db/lab_01/data/species.csv'
delimiter ';'
header csv;
