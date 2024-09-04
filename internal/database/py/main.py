from database import Database
from generate_data import InfoGenerator


def main():
    db = Database()
    db.drop_tables()
    db.create_tables()
    # g = InfoGenerator(5000)
    # g.generate_info()
    # db.copy_tables()


if __name__ == "__main__":
    main()
