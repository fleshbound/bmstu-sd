import faker
import faker_commerce
import random

from internal.database.py.dbconfig import DATA_TEST_PATH


class InfoGenerator:
    def __init__(self, rows=1000):
        self.CLIENTS_FILE = f"{DATA_TEST_PATH}/clients_info.csv"
        self.COMPANIES_FILE = f"{DATA_TEST_PATH}/companies_info.csv"
        self.MAILINGS_FILE = f"{DATA_TEST_PATH}/mailings_info.csv"
        self.MAILINGSERVICES_FILE = f"{DATA_TEST_PATH}/mailingservices_info.csv"
        self.MAILINGSUBSCRIPTIONS_FILE = f"{DATA_TEST_PATH}/mailingsubsriptions_info.csv"
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
