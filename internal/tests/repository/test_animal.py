import datetime

from pydantic import PositiveFloat, NonNegativeInt

from internal.src.container.container import Container
from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.utils.types import ID, AnimalName, Datetime, Sex, Weight, Height, Length
from internal.src.repository.sqlalchemy.animal import SqlAlchemyAnimalRepository


container = Container()


def animal_repository() -> SqlAlchemyAnimalRepository:
    return container.animal_repo()


def animalschema(id: NonNegativeInt,
                        user_id: NonNegativeInt,
                        breed_id: NonNegativeInt,
                        weight: PositiveFloat,
                        length: PositiveFloat,
                        height: PositiveFloat,
                        has_defects: bool,
                        is_multicolor: bool) -> AnimalSchema:
    return AnimalSchema(
            id=ID(id),
            user_id=ID(user_id),
            breed_id=ID(breed_id),
            name=AnimalName('Cool Animal Name'),
            birth_dt=Datetime(datetime.datetime(2020, 10, 15)),
            sex=Sex.male,
            weight=Weight(weight),
            height=Height(height),
            has_defects=has_defects,
            is_multicolor=is_multicolor,
            length=Length(length)
    )


def test_animal_create():
    animal = animalschema(0, 0, 0, 100, 100, 100, False, False)
    animal_repo = animal_repository()
    animal_repo.create(animal)
    assert animal_repo.get_by_id(0).id.value == 0
