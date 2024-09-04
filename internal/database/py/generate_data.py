from typing import List

import faker
import faker_commerce
import random

from Cryptodome.Hash import SHA256
from faker.providers import DynamicProvider

from internal.database.py.dbconfig import DATA_TEST_PATH

PATH = DATA_TEST_PATH

ANIMAL_PATH = f"{PATH}/animal.csv"
USER_PATH = f"{PATH}/user.csv"
USERSHOW_PATH = f"{PATH}/usershow.csv"
ANIMALSHOW_PATH = f"{PATH}/animalshow.csv"
STANDARD_PATH = f"{PATH}/standard.csv"
SHOW_PATH = f"{PATH}/show.csv"
WEIGHT_MAX = 100
LENGTH_MAX = 100
HEIGHT_MAX = 100


show_status_provider = DynamicProvider(
    provider_name='show_status',
    elements=['created', 'started', 'stopped', 'aborted']
)


show_class_provider = DynamicProvider(
    provider_name='show_class',
    elements=['one', 'two', 'three']
)

user_role_provider = DynamicProvider(
    provider_name='user_role',
    elements=['guest', 'judge', 'admin', 'breeder']
)


class InfoGenerator:
    def __init__(self, rows: int = 1000):
        self.ROWS = rows
        self.fake = faker.Faker()
        self.fake.add_provider(faker_commerce.Provider)
        self.fake.add_provider(show_status_provider)
        self.fake.add_provider(show_class_provider)
        self.fake.add_provider(user_role_provider)
        random.seed()

    def generate_info(self):
        print("Generating info... ", end="")

        print("DONE")

    def generate_animal_info(self):
        with open(ANIMAL_PATH, 'w') as f:
            for i in range(1, self.ROWS + 1):
                # copy animal(user_id, breed_id, name, birth_dt, sex, weight, height, length, has_defects, is_multicolor)
                user_id = random.randint(1, self.ROWS - 1)
                breed_id = random.randint(1, self.ROWS - 1)
                name = self.fake.name()
                birth_dt = self.fake.date_this_year()
                sex = ['male', 'female'][random.randint(0, 1)]
                weight = round(random.uniform(0.001, WEIGHT_MAX), 3)
                length = round(random.uniform(0.001, LENGTH_MAX), 3)
                height = round(random.uniform(0.001, HEIGHT_MAX), 3)
                has_defects = self.fake.boolean()
                is_multicolor = self.fake.boolean()
                animal_str = (f'{user_id};{breed_id};{name};{birth_dt};{sex};{weight};'
                              f'{height};{length};{has_defects};{is_multicolor}\n')
                f.write(animal_str)

    def generate_user_info(self):
        with open(USER_PATH, 'w') as f:
            for i in range(1, self.ROWS + 1):
                # copy "User"(email, hashed_password, role, name)
                email = self.fake.ascii_email()
                name = self.fake.name()
                hashed_password = SHA256.new(data=name.encode()).hexdigest()
                role = self.fake.user_role()
                user_str = f'{email};{hashed_password};{role};{name}\n'
                f.write(user_str)

    def generate_usershow_info(self):
        with open(USERSHOW_PATH, 'w') as f:
            for i in range(1, self.ROWS + 1):
                # copy UserShow (show_id, user_id, is_archived)
                show_id = random.randint(1, self.ROWS - 1)
                user_id = random.randint(1, self.ROWS - 1)
                is_archived = self.fake.boolean()
                usershow_str = f'{show_id};{user_id};{is_archived}\n'
                f.write(usershow_str)

    def generate_animalshow_info(self):
        with open(ANIMALSHOW_PATH, 'w') as f:
            for i in range(1, self.ROWS + 1):
                # copy AnimalShow (show_id, animal_id, is_archived)
                show_id = random.randint(1, self.ROWS - 1)
                animal_id = random.randint(1, self.ROWS - 1)
                is_archived = self.fake.boolean()
                animalshow_str = f'{show_id};{animal_id};{is_archived}\n'
                f.write(animalshow_str)

    def generate_standard_info(self):
        with open(STANDARD_PATH, 'w') as f:
            for i in range(1, self.ROWS + 1):
                # copy Standard (breed_id, country, weight, height, length, has_defects, is_multicolor, 
                # weight_delta_percent, height_delta_percent, length_delta_percent)
                breed_id = random.randint(1, self.ROWS - 1)
                country = self.fake.country()
                weight = round(random.uniform(0.001, WEIGHT_MAX), 3)
                length = round(random.uniform(0.001, LENGTH_MAX), 3)
                height = round(random.uniform(0.001, HEIGHT_MAX), 3)
                weight_delta_percent = round(random.uniform(0.01, 100), 2)
                length_delta_percent = round(random.uniform(0.01, 100), 2)
                height_delta_percent = round(random.uniform(0.01, 100), 2)
                has_defects = self.fake.boolean()
                is_multicolor = self.fake.boolean()
                show_str = (f'{breed_id};{country};{weight};{height};{length};{has_defects};{is_multicolor};'
                            f'{weight_delta_percent};{height_delta_percent};{length_delta_percent}\n')
                f.write(show_str)
    
    def generate_show_info(self):
        with open(SHOW_PATH, 'w') as f:
            for i in range(1, self.ROWS + 1):
                # copy Show (species_id, breed_id, standard_id, status, country, show_class, name, is_multi_breed)
                is_multi_breed = self.fake.boolean()
                breed_id = 'Null' if is_multi_breed else random.randint(1, self.ROWS - 1)
                standard_id = 'Null' if is_multi_breed else random.randint(1, self.ROWS - 1)
                species_id = 'Null' if not is_multi_breed else random.randint(1, self.ROWS - 1)
                status = self.fake.show_status()
                country = self.fake.country()
                show_class = self.fake.show_class()
                name = self.fake.company()
                show_str = (f'{species_id};{breed_id};{standard_id};{status};'
                            f'{country};{show_class};{name};{is_multi_breed}\n')
                f.write(show_str)

    #copy Species (name, group_id)
    # from '/home/sheglar/bmstu/db/lab_01/data/species.csv'
    # delimiter ';'
    # header csv;

    # copy "Group" (name)
    # from '/home/sheglar/bmstu/db/lab_01/data/group.csv'
    # delimiter ';'
    # header csv;
    #
    # copy Breed (name, species_id)
    # from '/home/sheglar/bmstu/db/lab_01/data/breed.csv'
    # delimiter ';'
    # header csv;
    #
    # copy Certificate (animalshow_id, rank)
    # from '/home/sheglar/bmstu/db/lab_01/data/species.csv'
    # delimiter ';'
    # header csv;
