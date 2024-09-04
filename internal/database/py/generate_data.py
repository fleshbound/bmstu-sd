from typing import List

import faker
import faker_commerce
import random

from Cryptodome.Hash import SHA256

from internal.database.py.dbconfig import DATA_TEST_PATH

ANIMAL_PATH = f"{DATA_TEST_PATH}/animal.csv"
USER_PATH = f"{DATA_TEST_PATH}/user.csv"
USERSHOW_PATH = f"{DATA_TEST_PATH}/usershow.csv"
WEIGHT_MAX = 100
LENGTH_MAX = 100
HEIGHT_MAX = 100


class InfoGenerator:
    def __init__(self, rows: int = 1000):
        self.ROWS = rows
        self.fake = faker.Faker()
        self.fake.add_provider(faker_commerce.Provider)
        random.seed()

    def generate_info(self):
        print("Generating info... ", end="")
        self.generate_clients_info()
        self.generate_companies_info()
        self.generate_mailingservices_info()
        self.generate_mailingsubscriptions_info()
        self.generate_mailings_info()
        print("DONE")

    def generate_clients_info(self):
        with open(self.CLIENTS_FILE, "w") as f:
            for i in range(1, self.ROWS + 1):
                favourite_client_id = random.randint(1, self.ROWS - 1)
                email = self.fake.ascii_email()
                name = self.fake.name()
                age = random.randint(13, 100)
                sum_purchase_dollars = round(random.uniform(0, 1000), 2)
                client_str = f"{favourite_client_id};{email};{name};{age};{sum_purchase_dollars}\n"
                # f.write("id;favourite_client_id;email;name;age;sum_purchase_dollars\n")
                f.write(client_str)

    def generate_companies_info(self):
        with open(self.COMPANIES_FILE, "w") as f:
            for i in range(1, self.ROWS + 1):
                name = self.fake.company()
                country = self.fake.country()
                revenue_dollars = round(random.uniform(10000, 1000000), 2)
                email = self.fake.company_email()
                company_str = f"{name};{country};{revenue_dollars};{email}\n"
                # f.write("id;name;country;revenue_dollars;email\n")
                f.write(company_str)

    def generate_mailingservices_info(self):
        with open(self.MAILINGSERVICES_FILE, "w") as f:
            for i in range(1, self.ROWS + 1):
                name = self.fake.ecommerce_name()
                is_messenger = self.fake.boolean()
                response_speed_ms = round(random.uniform(0.000001, 9), 6)
                version = self.fake.random_int(min=0, max=100)
                mailingservice_str = f"{is_messenger};{response_speed_ms};{version};{name}\n"
                # f.write("id;is_messenger;response_speed_ms;version;name\n")
                f.write(mailingservice_str)

    def generate_mailings_info(self):
        with open(self.MAILINGS_FILE, "w") as f:
            for i in range(1, self.ROWS + 1):
                company_id = random.randint(1, self.ROWS - 1)
                mailing_service_id = random.randint(1, self.ROWS - 1)
                is_periodic = self.fake.boolean()
                period_days = 0 if is_periodic == False else random.randint(1, 365)
                mailing_str = f"{company_id};{mailing_service_id};{is_periodic};{period_days}\n"
                # f.write("company_id;mailing_service_id;is_periodic;period_days\n")
                f.write(mailing_str)

    def generate_mailingsubscriptions_info(self):
        with open(self.MAILINGSUBSCRIPTIONS_FILE, "w") as f:
            for i in range(1, self.ROWS + 1):
                client_id = random.randint(1, self.ROWS - 1)
                mailing_service_id = random.randint(1, self.ROWS - 1)
                price_dollars = round(random.uniform(0, 10), 2)
                start_at = self.fake.date_time_this_year()
                mailingsubscription_str = f"{client_id};{mailing_service_id};{price_dollars};{start_at}\n"
                # f.write("client_id;mailing_service_id;price_dollars;start_at\n")
                f.write(mailingsubscription_str)

    def generate_animal_info(self):
        with open(ANIMAL_PATH, 'w') as f:
            for i in range(1, self.ROWS + 1):
                # copy animal(user_id, breed_id, name, birth_dt, sex, weight, height, length, has_defects, is_multicolor)
                user_id = random.randint(1, self.ROWS - 1)
                breed_id = random.randint(1, self.ROWS - 1)
                name = self.fake.name()
                birth_dt = self.fake.date_this_year()
                sex = ['male', 'female'][random.randint(0, 1)]
                weight = random.random() * WEIGHT_MAX
                length = random.random() * LENGTH_MAX
                height = random.random() * HEIGHT_MAX
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
                role = ['guest', 'judge', 'admin', 'breeder'][self.fake.random_int(min=0, max=3)]
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
        with open(USERSHOW_PATH, 'w') as f:
            for i in range(1, self.ROWS + 1):
                # copy AnimalShow (show_id, animal_id, is_archived)
                show_id = random.randint(1, self.ROWS - 1)
                animal_id = random.randint(1, self.ROWS - 1)
                is_archived = self.fake.boolean()
                animalshow_str = f'{show_id};{animal_id};{is_archived}\n'
                f.write(animalshow_str)

    def generate_standard_indo(self):
        pass
