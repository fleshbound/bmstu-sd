import os
import random

import faker
import faker_commerce
from Cryptodome.Hash import SHA256
from faker.providers import DynamicProvider

COUNTRIES=['Afghanistan',
        'Albania',
        'Algeria',
        'Andorra',
        'Angola',
        'Antigua & Deps',
        'Argentina',
        'Armenia',
        'Australia',
        'Austria',
        'Azerbaijan',
        'Bahamas',
        'Bahrain',
        'Bangladesh',
        'Barbados',
        'Belarus',
        'Belgium',
        'Belize',
        'Benin',
        'Bermuda',
        'Bhutan',
        'Bolivia',
        'Bosnia Herzegovina',
        'Botswana',
        'Brazil',
        'Brunei',
        'Bulgaria',
        'Burkina',
        'Burundi',
        'Cambodia',
        'Cameroon',
        'Canada',
        'Cape Verde',
        'Central African Rep',
        'Chad',
        'Chile',
        'China',
        'Colombia',
        'Comoros',
        'Congo',
        'Congo (Democratic Rep)',
        'Costa Rica',
        'Croatia',
        'Cuba',
        'Cyprus',
        'Czech Republic',
        'Denmark',
        'Djibouti',
        'Dominica',
        'Dominican Republic',
        'East Timor',
        'Ecuador',
        'Egypt',
        'El Salvador',
        'Equatorial Guinea',
        'Eritrea',
        'Estonia',
        'Eswatini',
        'Ethiopia',
        'Fiji',
        'Finland',
        'France',
        'Gabon',
        'Gambia',
        'Georgia',
        'Germany',
        'Ghana',
        'Greece',
        'Grenada',
        'Guatemala',
        'Guinea',
        'Guinea-Bissau',
        'Guyana',
        'Haiti',
        'Honduras',
        'Hungary',
        'Iceland',
        'India',
        'Indonesia',
        'Iran',
        'Iraq',
        'Ireland (Republic)',
        'Israel',
        'Italy',
        'Ivory Coast',
        'Jamaica',
        'Japan',
        'Jordan',
        'Kazakhstan',
        'Kenya',
        'Kiribati',
        'Korea North',
        'Korea South',
        'Kosovo',
        'Kuwait',
        'Kyrgyzstan',
        'Laos',
        'Latvia',
        'Lebanon',
        'Lesotho',
        'Liberia',
        'Libya',
        'Liechtenstein',
        'Lithuania',
        'Luxembourg',
        'Macedonia',
        'Madagascar',
        'Malawi',
        'Malaysia',
        'Maldives',
        'Mali',
        'Malta',
        'Marshall Islands',
        'Mauritania',
        'Mauritius',
        'Mexico',
        'Micronesia',
        'Moldova',
        'Monaco',
        'Mongolia',
        'Montenegro',
        'Morocco',
        'Mozambique',
        'Myanmar',
        'Namibia',
        'Nauru',
        'Nepal',
        'Netherlands',
        'New Zealand',
        'Nicaragua',
        'Niger',
        'Nigeria',
        'Norway',
        'Oman',
        'Pakistan',
        'Palau',
        'Palestine',
        'Panama',
        'Papua New Guinea',
        'Paraguay',
        'Peru',
        'Philippines',
        'Poland',
        'Portugal',
        'Qatar',
        'Romania',
        'Russian Federation',
        'Rwanda',
        'St Kitts & Nevis',
        'St Lucia',
        'Saint Vincent & the Grenadines',
        'Samoa',
        'San Marino',
        'Sao Tome & Principe',
        'Saudi Arabia',
        'Senegal',
        'Serbia',
        'Seychelles',
        'Sierra Leone',
        'Singapore',
        'Slovakia',
        'Slovenia',
        'Solomon Islands',
        'Somalia',
        'South Africa',
        'South Sudan',
        'Spain',
        'Sri Lanka',
        'Sudan',
        'Suriname',
        'Sweden',
        'Switzerland',
        'Syria',
        'Taiwan',
        'Tajikistan',
        'Tanzania',
        'Thailand',
        'Togo',
        'Tonga',
        'Trinidad & Tobago',
        'Tunisia',
        'Turkey',
        'Turkmenistan',
        'Tuvalu',
        'Uganda',
        'Ukraine',
        'United Arab Emirates',
        'United Kingdom',
        'United States',
        'Uruguay',
        'Uzbekistan',
        'Vanuatu',
        'Vatican City',
        'Venezuela',
        'Vietnam',
        'Yemen',
        'Zambia',
        'Zimbabwe']

show_status_provider = DynamicProvider(
    provider_name='show_status',
    elements=['created', 'started', 'stopped']
)


show_class_provider = DynamicProvider(
    provider_name='show_class',
    elements=['one', 'two', 'three']
)

user_role_provider = DynamicProvider(
    provider_name='user_role',
    elements=['guest', 'judge', 'admin', 'breeder']
)

mycountry_provider = DynamicProvider(
    provider_name='mycountry',
    elements=COUNTRIES
)

groups = ['fish', 'amphibians', 'reptiles', 'birds', 'mammals']


class InfoGenerator:
    group_max_id: int
    species_max_id: int
    breed_max_id: int

    def __init__(self, rows: int):
        self.PATH = os.getenv("DATA_PATH")

        # PATH = "/app/database/data"
        self.ANIMAL_PATH = f"{self.PATH}/animal.csv"
        self.USER_PATH = f"{self.PATH}/user.csv"
        self.USERSHOW_PATH = f"{self.PATH}/usershow.csv"
        self.ANIMALSHOW_PATH = f"{self.PATH}/animalshow.csv"
        self.STANDARD_PATH = f"{self.PATH}/standard.csv"
        self.GROUP_PATH = f"{self.PATH}/group.csv"
        self.SPECIES_PATH = f"{self.PATH}/species.csv"
        self.BREED_PATH = f"{self.PATH}/breed.csv"
        self.SHOW_PATH = f"{self.PATH}/show.csv"
        self.WEIGHT_MAX = 100
        self.LENGTH_MAX = 100
        self.HEIGHT_MAX = 100
        
        self.ROWS = rows
        self.fake = faker.Faker()
        self.fake.add_provider(faker_commerce.Provider)
        self.fake.add_provider(show_status_provider)
        self.fake.add_provider(show_class_provider)
        self.fake.add_provider(user_role_provider)
        self.fake.add_provider(mycountry_provider)
        random.seed()

    def generate_test_info(self):
        self.USER_PATH = f"{os.getenv('DATA_TEST_PATH')}/{self.ROWS}.csv"
        print(self.USER_PATH)
        self.generate_user_info_real()

    def generate_info(self):
        print("Generating info... ", end="")
        self.generate_user_info()
        self.generate_group_info()
        self.generate_species_info()
        self.generate_breed_info()
        self.generate_animal_info()
        self.generate_standard_info()
        self.generate_show_info()
        self.generate_usershow_info()
        self.generate_animalshow_info()
        print("DONE")

    def generate_animal_info(self):
        # copy animal(user_id, breed_id, name, birth_dt, sex, weight, height, length, has_defects, is_multicolor)
        with open(self.ANIMAL_PATH, 'w+') as f:
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

            for i in range(1, self.ROWS + 1):
                user_id = i
                breed_id = i
                name = self.fake.name()
                birth_dt = self.fake.date_this_year()
                sex = ['male', 'female'][random.randint(0, 1)]
                weight = round(self.WEIGHT_MAX, 3)
                length = round(self.LENGTH_MAX, 3)
                height = round(self.HEIGHT_MAX, 3)
                has_defects = 'false'
                is_multicolor = 'false'
                animal_str = (f'{user_id};{breed_id};{name};{birth_dt};{sex};{weight};'
                              f'{height};{length};{has_defects};{is_multicolor}\n')
                f.write(animal_str)

    def generate_user_info_real(self):
        with open(self.USER_PATH, 'w+') as f:
            f.write('email;hashed_password;role;name\n')
            for i in range(self.ROWS):
                email = self.fake.ascii_email()
                name = self.fake.name()
                hashed_password = SHA256.new(data=name.encode()).hexdigest()
                role = self.fake.user_role()
                user_str = f'{email};{hashed_password};{role};{name}\n'
                f.write(user_str)

    def generate_user_info(self):
        # copy "User"(email, hashed_password, role, name)
        with open(self.USER_PATH, 'w+') as f:
            f.write('email;hashed_password;role;name\n')
            for i in range(self.ROWS):
                email = self.fake.ascii_email()
                name = self.fake.name()
                hashed_password = SHA256.new(data=name.encode()).hexdigest()
                role = 'breeder'
                user_str = f'{email};{hashed_password};{role};{name}\n'
                f.write(user_str)

            for i in range(100):
                email = self.fake.ascii_email()
                name = self.fake.name()
                hashed_password = SHA256.new(data=name.encode()).hexdigest()
                role = 'judge'
                user_str = f'{email};{hashed_password};{role};{name}\n'
                f.write(user_str)

            for i in range(100):
                email = self.fake.ascii_email()
                name = self.fake.name()
                hashed_password = SHA256.new(data=name.encode()).hexdigest()
                role = 'admin'
                user_str = f'{email};{hashed_password};{role};{name}\n'
                f.write(user_str)

            for i in range(100):
                email = self.fake.ascii_email()
                name = self.fake.name()
                hashed_password = SHA256.new(data=name.encode()).hexdigest()
                role = 'guest'
                user_str = f'{email};{hashed_password};{role};{name}\n'
                f.write(user_str)

    def generate_usershow_info(self):
        # copy UserShow (show_id, user_id, is_archived)
        with open(self.USERSHOW_PATH, 'w+') as f:
            f.write('show_id;user_id;is_archived\n')
            for i in range(1, self.ROWS + 1):
                show_id = i
                user_id = random.randint(self.ROWS + 1, self.ROWS + 100)
                is_archived = False  # self.fake.boolean()
                usershow_str = f'{show_id};{user_id};{is_archived}\n'
                f.write(usershow_str)

    def generate_animalshow_info(self):
        with open(self.ANIMALSHOW_PATH, 'w+') as f:
            for i in range(self.ROWS + 1, 2 * self.ROWS + 1):
                # copy AnimalShow (show_id, animal_id, is_archived)
                show_id = i
                animal_id = i
                is_archived = False  # self.fake.boolean()
                animalshow_str = f'{show_id};{animal_id};{is_archived}\n'
                f.write(animalshow_str)

    def generate_standard_info(self):
        # copy Standard (breed_id, country, weight, height, length, has_defects, is_multicolor,
        # weight_delta_percent, height_delta_percent, length_delta_percent)
        with open(self.STANDARD_PATH, 'w+') as f:
            f.write('breed_id;country;weight;height;length;has_defects;is_multicolor;'
                    + 'weight_delta_percent;height_delta_percent;length_delta_percent\n')
            for i in range(1, self.ROWS + 1):
                breed_id = i  # random.randint(1, self.breed_max_id)
                country = self.fake.mycountry()
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

            for i in range(1, self.ROWS + 1):
                breed_id = i  # random.randint(1, self.breed_max_id)
                country = self.fake.mycountry()
                weight = round(self.WEIGHT_MAX, 3)
                length = round(self.LENGTH_MAX, 3)
                height = round(self.HEIGHT_MAX, 3)
                weight_delta_percent = 10
                length_delta_percent = 10
                height_delta_percent = 10
                has_defects = 'false'
                is_multicolor = 'false'
                show_str = (f'{breed_id};{country};{weight};{height};{length};{has_defects};{is_multicolor};'
                            f'{weight_delta_percent};{height_delta_percent};{length_delta_percent}\n')
                f.write(show_str)

    def generate_show_info(self):
        # copy Show (species_id, breed_id, standard_id, status, country, show_class, name, is_multi_breed)
        with open(self.SHOW_PATH, 'w+') as f:
            f.write('species_id;breed_id;standard_id;status;country;show_class;name;is_multi_breed\n')
            for i in range(1, self.ROWS + 1):
                is_multi_breed = self.fake.boolean()
                breed_id = '' if is_multi_breed else i  # random.randint(1, self.breed_max_id)
                standard_id = '' if is_multi_breed else i
                species_id = '' if not is_multi_breed else random.randint(1, self.ROWS - 1)
                status = 'created'  # self.fake.show_status()
                country = self.fake.mycountry()
                show_class = self.fake.show_class()
                name = self.fake.company()
                show_str = (f'{species_id};{breed_id};{standard_id};{status};'
                            f'{country};{show_class};{name};{is_multi_breed}\n')
                f.write(show_str)

            for i in range(self.ROWS + 1, 2 * self.ROWS + 1):
                is_multi_breed = 'false'
                breed_id = i - self.ROWS
                standard_id = i
                species_id = ''
                status = 'created' #  self.fake.show_status()
                country = self.fake.mycountry()
                show_class = self.fake.show_class()
                name = self.fake.company()
                show_str = (f'{species_id};{breed_id};{standard_id};{status};'
                            f'{country};{show_class};{name};{is_multi_breed}\n')
                f.write(show_str)

    def generate_group_info(self):
        # copy "Group" (name)
        with open(self.GROUP_PATH, 'w+') as f:
            f.write('name\n')
            for g_name in groups:
                f.write(f'{g_name}\n')
        self.group_max_id = len(groups)

    def generate_species_info(self):
        # copy Species (name, group_id)
        with open(self.SPECIES_PATH, 'w+') as f:
            f.write('name;group_id\n')
            for i in range(self.ROWS):
                group_id = random.randint(1, self.group_max_id - 1)
                name = self.fake.name() + ' ' + self.fake.color()
                f.write(f'{name};{group_id}\n')
        self.species_max_id = self.ROWS

    def generate_breed_info(self):
        # copy Breed (name, species_id)
        with open(self.BREED_PATH, 'w+') as f:
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
