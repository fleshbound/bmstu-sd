import os
import random

import faker
import faker_commerce
from Cryptodome.Hash import SHA256
from faker.providers import DynamicProvider

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

groups = ['fish', 'amphibians', 'reptiles', 'birds', 'mammals']


class InfoGenerator:
    group_max_id: int
    species_max_id: int
    breed_max_id: int

    def __init__(self, rows: int = 1000):
        PATH = os.getenv("DATA_TEST_PATH")

        self.ANIMAL_PATH = f"{PATH}/animal.csv"
        self.USER_PATH = f"{PATH}/user.csv"
        self.USERSHOW_PATH = f"{PATH}/usershow.csv"
        self.ANIMALSHOW_PATH = f"{PATH}/animalshow.csv"
        self.STANDARD_PATH = f"{PATH}/standard.csv"
        self.GROUP_PATH = f"{PATH}/group.csv"
        self.SPECIES_PATH = f"{PATH}/species.csv"
        self.BREED_PATH = f"{PATH}/breed.csv"
        self.SHOW_PATH = f"{PATH}/show.csv"
        self.WEIGHT_MAX = 100
        self.LENGTH_MAX = 100
        self.HEIGHT_MAX = 100
        
        self.ROWS = rows
        self.fake = faker.Faker()
        self.fake.add_provider(faker_commerce.Provider)
        self.fake.add_provider(show_status_provider)
        self.fake.add_provider(show_class_provider)
        self.fake.add_provider(user_role_provider)
        random.seed()

    def generate_info(self):
        print("Generating info... ", end="")
        self.generate_user_info()
        self.generate_group_info()
        self.generate_species_info()
        self.generate_breed_info()
        self.generate_animal_info()
        self.generate_standard_info()
        self.generate_show_info()
        print("DONE")

    def generate_animal_info(self):
        # copy animal(user_id, breed_id, name, birth_dt, sex, weight, height, length, has_defects, is_multicolor)
        with open(self.ANIMAL_PATH, 'w') as f:
            f.write('user_id;breed_id;name;birth_dt;sex;weight;height;length;has_defects;is_multicolor\n')
            for i in range(self.ROWS):
                user_id = random.randint(1, self.ROWS - 1)
                breed_id = random.randint(1, self.breed_max_id)
                name = self.fake.name()
                birth_dt = self.fake.date_this_year()
                sex = ['male', 'female'][random.randint(0, 1)]
                weight = round(random.uniform(0.001, self.WEIGHT_MAX), 3)
                length = round(random.uniform(0.001, self.LENGTH_MAX), 3)
                height = round(random.uniform(0.001, self.HEIGHT_MAX), 3)
                has_defects = self.fake.boolean()
                is_multicolor = self.fake.boolean()
                animal_str = (f'{user_id};{breed_id};{name};{birth_dt};{sex};{weight};'
                              f'{height};{length};{has_defects};{is_multicolor}\n')
                f.write(animal_str)

    def generate_user_info(self):
        # copy "User"(email, hashed_password, role, name)
        with open(self.USER_PATH, 'w') as f:
            f.write('email;hashed_password;role;name\n')
            for i in range(self.ROWS):
                email = self.fake.ascii_email()
                name = self.fake.name()
                hashed_password = SHA256.new(data=name.encode()).hexdigest()
                role = self.fake.user_role()
                user_str = f'{email};{hashed_password};{role};{name}\n'
                f.write(user_str)

    def generate_usershow_info(self):
        # copy UserShow (show_id, user_id, is_archived)
        with open(self.USERSHOW_PATH, 'w') as f:
            f.write('show_id;user_id;is_archived\n')
            for i in range(self.ROWS):
                show_id = random.randint(1, self.ROWS - 1)
                user_id = random.randint(1, self.ROWS - 1)
                is_archived = False  # self.fake.boolean()
                usershow_str = f'{show_id};{user_id};{is_archived}\n'
                f.write(usershow_str)

    # def generate_animalshow_info(self):
    #     with open(self.ANIMALSHOW_PATH, 'w') as f:
    #         for i in range(self.ROWS):
    #             # copy AnimalShow (show_id, animal_id, is_archived)
    #             show_id = random.randint(1, self.ROWS - 1)
    #             animal_id = random.randint(1, self.ROWS - 1)
    #             is_archived = False  # self.fake.boolean()
    #             animalshow_str = f'{show_id};{animal_id};{is_archived}\n'
    #             f.write(animalshow_str)

    def generate_standard_info(self):
        # copy Standard (breed_id, country, weight, height, length, has_defects, is_multicolor,
        # weight_delta_percent, height_delta_percent, length_delta_percent)
        with open(self.STANDARD_PATH, 'w') as f:
            f.write('breed_id;country;weight;height;length;has_defects;is_multicolor;'
                    + 'weight_delta_percent;height_delta_percent;length_delta_percent\n')
            for i in range(1, self.ROWS + 1):
                breed_id = i  # random.randint(1, self.breed_max_id)
                country = self.fake.country()
                weight = round(random.uniform(0.001, self.WEIGHT_MAX), 3)
                length = round(random.uniform(0.001, self.LENGTH_MAX), 3)
                height = round(random.uniform(0.001, self.HEIGHT_MAX), 3)
                weight_delta_percent = round(random.uniform(0.01, 100), 2)
                length_delta_percent = round(random.uniform(0.01, 100), 2)
                height_delta_percent = round(random.uniform(0.01, 100), 2)
                has_defects = self.fake.boolean()
                is_multicolor = self.fake.boolean()
                show_str = (f'{breed_id};{country};{weight};{height};{length};{has_defects};{is_multicolor};'
                            f'{weight_delta_percent};{height_delta_percent};{length_delta_percent}\n')
                f.write(show_str)

    def generate_show_info(self):
        # copy Show (species_id, breed_id, standard_id, status, country, show_class, name, is_multi_breed)
        with open(self.SHOW_PATH, 'w') as f:
            f.write('species_id;breed_id;standard_id;status;country;show_class;name;is_multi_breed\n')
            for i in range(1, self.ROWS + 1):
                is_multi_breed = self.fake.boolean()
                breed_id = '' if is_multi_breed else i  # random.randint(1, self.breed_max_id)
                standard_id = '' if is_multi_breed else i
                species_id = '' if not is_multi_breed else random.randint(1, self.ROWS - 1)
                status = 'created'  # self.fake.show_status()
                country = self.fake.country()
                show_class = self.fake.show_class()
                name = self.fake.company()
                show_str = (f'{species_id};{breed_id};{standard_id};{status};'
                            f'{country};{show_class};{name};{is_multi_breed}\n')
                f.write(show_str)

    def generate_group_info(self):
        # copy "Group" (name)
        with open(self.GROUP_PATH, 'w') as f:
            f.write('name\n')
            for g_name in groups:
                f.write(f'{g_name}\n')
        self.group_max_id = len(groups)

    def generate_species_info(self):
        # copy Species (name, group_id)
        with open(self.SPECIES_PATH, 'w') as f:
            f.write('name;group_id\n')
            for i in range(self.ROWS):
                group_id = random.randint(1, self.group_max_id - 1)
                name = self.fake.name() + ' ' + self.fake.color()
                f.write(f'{name};{group_id}\n')
        self.species_max_id = self.ROWS

    def generate_breed_info(self):
        # copy Breed (name, species_id)
        with open(self.BREED_PATH, 'w') as f:
            f.write('name;species_id\n')
            for i in range(self.ROWS):
                species_id = random.randint(1, self.species_max_id)
                name = 'Breed ' + self.fake.color()
                f.write(f'{name};{species_id}\n')
        self.breed_max_id = self.ROWS

    # copy Certificate (animalshow_id, rank)
    # from '/home/sheglar/bmstu/db/lab_01/data/species.csv'
    # delimiter ';'
    # header csv;

    # score
