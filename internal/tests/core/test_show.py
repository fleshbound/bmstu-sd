import datetime
from typing import Optional, List

import pytest
from fastapi import HTTPException
from pydantic import NonNegativeInt, PositiveFloat

from internal.src.core.breed.schema.breed import BreedSchema
from internal.src.core.certificate.schema.certificate import CertificateSchema
from internal.src.core.show.schema.animalshow import AnimalShowSchema
from internal.src.core.show.schema.usershow import UserShowSchema
from internal.src.core.species.schema.species import SpeciesSchema
from internal.src.core.user.schema.user import UserSchema, UserRole
from internal.src.core.utils.exceptions import CreateShowMultiBreedError, CreateShowSingleBreedError, \
    StartShowStatusError, StartShowZeroRecordsError, StopShowStatusError, RegisterShowStatusError, \
    RegisterAnimalCheckError, RegisterUserRoleError, RegisterUserRegisteredError, UnregisterShowStatusError, \
    UnregisterAnimalNotRegisteredError, UnregisterUserNotRegisteredError, StopNotAllUsersScoredError, \
    RegisterAnimalRegisteredError
from internal.tests.core.mock.repo.show import MockedShowRepository
from internal.tests.core.mock.service.animal import MockedAnimalService
from internal.tests.core.mock.service.animalshow import MockedAnimalShowService
from internal.tests.core.mock.service.breed import MockedBreedService
from internal.tests.core.mock.service.certificate import MockedCertificateService
from internal.tests.core.mock.service.score import MockedScoreService
from internal.tests.core.mock.service.standard import MockedStandardService
from internal.tests.core.mock.service.user import MockedUserService
from internal.tests.core.mock.service.usershow import MockedUserShowService
from internal.src.core.show.schema.score import ScoreSchema
from internal.src.core.standard.schema.standard import StandardSchema
from internal.src.core.animal.schema.animal import AnimalSchema
from internal.src.core.show.schema.show import ShowSchema, ShowStatus, ShowClass, ShowSchemaCreate, \
    ShowRegisterAnimalStatus, ShowRegisterUserStatus
from internal.src.core.utils.types import ID, Country, Weight, Height, Length, AnimalName, Datetime, Sex, ShowName, \
    BreedName, Email, HashedPassword, UserName, SpeciesName
from internal.src.core.show.service.impl.show import ShowService


def mocked_standardschema(id: NonNegativeInt,
                          breed_id: NonNegativeInt,
                          weight: PositiveFloat,
                          length: PositiveFloat,
                          height: PositiveFloat,
                          has_defects: bool,
                          is_multicolor: bool,
                          weight_delta_percent: PositiveFloat,
                          height_delta_percent: PositiveFloat,
                          length_delta_percent: PositiveFloat) -> StandardSchema:
    return StandardSchema(
        id=ID(id),
        breed_id=ID(breed_id),
        country=Country('Russian Federation'),
        weight=Weight(weight),
        height=Height(height),
        has_defects=has_defects,
        is_multicolor=is_multicolor,
        length=Length(length),
        weight_delta_percent=weight_delta_percent,
        height_delta_percent=height_delta_percent,
        length_delta_percent=length_delta_percent
    )


def mocked_animalschema(id: NonNegativeInt,
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


def mocked_showschema(id: NonNegativeInt = 0,
                      status: ShowStatus = ShowStatus.created,
                      species_id: Optional[NonNegativeInt] = None,
                      breed_id: Optional[NonNegativeInt] = 0,
                      standard_id: Optional[NonNegativeInt] = 0,
                      is_multi_breed: bool = False):
    return ShowSchema(
        id=ID(id),
        status=status,
        name=ShowName('Cool Show Name'),
        species_id=ID(species_id),
        breed_id=ID(breed_id),
        country=Country('Russian Federation'),
        show_class=ShowClass.one,
        standard_id=ID(standard_id),
        is_multi_breed=is_multi_breed
    )


def show_service_create(shows: List[ShowSchema],
                        scores: List[ScoreSchema],
                        animalshows: List[AnimalShowSchema],
                        usershows: List[UserShowSchema],
                        certificates: List[CertificateSchema],
                        animals: List[AnimalSchema],
                        users: List[UserSchema],
                        breeds: List[BreedSchema],
                        standards: List[StandardSchema]):
    return ShowService(
                 MockedShowRepository(shows),
                 score_service=MockedScoreService(scores),
                 animalshow_service=MockedAnimalShowService(animalshows),
                 usershow_service=MockedUserShowService(usershows),
                 certificate_service=MockedCertificateService(certificates),
                 animal_service=MockedAnimalService(animals),
                 user_service=MockedUserService(users),
                 breed_service=MockedBreedService(breeds),
                 standard_service=MockedStandardService(standards)
    )


def mocked_showschemacreate(
        species_id: Optional[NonNegativeInt],
        breed_id: Optional[NonNegativeInt],
        standard_id: Optional[NonNegativeInt],
        is_multi_breed: bool):
    if not species_id is None:
        species_id = ID(species_id)
    if not breed_id is None:
        breed_id = ID(breed_id)
    if not standard_id is None:
        standard_id = ID(standard_id)
    return ShowSchemaCreate(
        species_id=species_id,
        breed_id=breed_id,
        country=Country('Russian Federation'),
        show_class=ShowClass.one,
        name=ShowName('Cool Show Name'),
        standard_id=standard_id,
        is_multi_breed=is_multi_breed
    )


def mocked_usershowschema(id: NonNegativeInt,
                          user_id: NonNegativeInt,
                          show_id: NonNegativeInt,
                          is_archived: bool):
    return UserShowSchema(
        id=ID(id),
        user_id=ID(user_id),
        show_id=ID(show_id),
        is_archived=is_archived
    )


def mocked_animalshowschema(id: NonNegativeInt,
                            animal_id: NonNegativeInt,
                            show_id: NonNegativeInt,
                            is_archived: bool):
    return AnimalShowSchema(
        id=ID(id),
        animal_id=ID(animal_id),
        show_id=ID(show_id),
        is_archived=is_archived
    )


def mocked_breedschema(
    id: NonNegativeInt,
    species_id: NonNegativeInt
):
    return BreedSchema(
        id=ID(id),
        species_id=ID(species_id),
        name=BreedName('Cool Breed Name')
    )


def mocked_userschema(id: NonNegativeInt, role: UserRole):
    return UserSchema(
            id=ID(id),
            email=Email('coolemail@gmail.com'),
            hashed_password=HashedPassword('coolpass'),
            role=role,
            name=UserName('Cool Bob')
        )


def test_create_multibreed_yesbreed_error():
    create_show = mocked_showschemacreate(0, 0, None, True)
    show_service = show_service_create([], [], [], [], [], [], [], [], [])
    with pytest.raises(CreateShowMultiBreedError) as e:
        show_service.create(create_show)


def test_create_multibreed_nospecies_error():
    create_show = mocked_showschemacreate(None, None, None, True)
    show_service = show_service_create([], [], [], [], [], [], [], [], [])
    with pytest.raises(CreateShowMultiBreedError):
        show_service.create(create_show)


def test_create_multibreed_yesstandard_error():
    create_show = mocked_showschemacreate(0, None, 0, True)
    show_service = show_service_create([], [], [], [], [], [], [], [], [])
    with pytest.raises(CreateShowMultiBreedError):
        show_service.create(create_show)


def test_create_multibreed_ok():
    create_show = mocked_showschemacreate(0, None, None, True)
    show_service = show_service_create([], [], [], [], [], [], [], [], [])
    assert show_service.create(create_show).status == ShowStatus.created


def test_create_singlebreed_nostandard_error():
    create_show = mocked_showschemacreate(None, 0, None, False)
    show_service = show_service_create([], [], [], [], [], [], [], [], [])
    with pytest.raises(CreateShowSingleBreedError):
        show_service.create(create_show)


def test_create_singlebreed_yesspecies_error():
    create_show = mocked_showschemacreate(0, 0, 0, False)
    show_service = show_service_create([], [], [], [], [], [], [], [], [])
    with pytest.raises(CreateShowSingleBreedError):
        show_service.create(create_show)


def test_create_singlebreed_nobreed_error():
    create_show = mocked_showschemacreate(None, None, 0, False)
    show_service = show_service_create([], [], [], [], [], [], [], [], [])
    with pytest.raises(CreateShowSingleBreedError):
        show_service.create(create_show)


def test_create_singlebreed_ok():
    create_show = mocked_showschemacreate(None, 0, 0, False)
    show_service = show_service_create([], [], [], [], [], [], [], [], [])
    assert show_service.create(create_show).status == ShowStatus.created


def test_get_usershow_count_nonzero():
    shows = [mocked_showschema(0)]
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], [], usershows, [], [], [], [], [])
    assert show_service.get_usershow_count(ID(0)) == 1


def test_get_usershow_count_zero():
    shows = [mocked_showschema(0)]
    usershows = []
    show_service = show_service_create(shows, [], [], usershows, [], [], [], [], [])
    assert show_service.get_usershow_count(ID(0)) == 0


def test_get_animalshow_count_nonzero():
    shows = [mocked_showschema(0)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, [], [], [], [], [], [])
    assert show_service.get_animalshow_count(ID(0)) == 1


def test_get_animalshow_count_zero():
    shows = [mocked_showschema(0)]
    animalshows = []
    show_service = show_service_create(shows, [], animalshows, [], [], [], [], [], [])
    assert show_service.get_animalshow_count(ID(0)) == 0


def test_start_started_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.started)]
    show_service = show_service_create(shows, [], [], [], [], [], [], [], [])
    with pytest.raises(StartShowStatusError):
        show_service.start(ID(0))


def test_start_stopped_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.stopped)]
    show_service = show_service_create(shows, [], [], [], [], [], [], [], [])
    with pytest.raises(StartShowStatusError):
        show_service.start(ID(0))


def test_start_aborted_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.aborted)]
    show_service = show_service_create(shows, [], [], [], [], [], [], [], [])
    with pytest.raises(StartShowStatusError):
        show_service.start(ID(0))


def test_start_nousershows_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    usershows = [mocked_usershowschema(0, 1, 1, False)]
    show_service = show_service_create(shows, [], [], usershows, [], [], [], [], [])
    with pytest.raises(StartShowZeroRecordsError):
        show_service.start(ID(0))


def test_start_noanimalshows_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    animalshows = [mocked_animalshowschema(0, 1, 1, False)]
    show_service = show_service_create(shows, [], animalshows, [], [], [], [], [], [])
    with pytest.raises(StartShowZeroRecordsError):
        show_service.start(ID(0))


def test_start_ok():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, usershows, [], [], [], [], [])
    assert show_service.start(ID(0)).status == ShowStatus.started


def test_stop_created_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    show_service = show_service_create(shows, [], [], [], [], [], [], [], [])
    with pytest.raises(StopShowStatusError):
        show_service.stop(ID(0))


def test_stop_stopped_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.stopped)]
    show_service = show_service_create(shows, [], [], [], [], [], [], [], [])
    with pytest.raises(StopShowStatusError):
        show_service.stop(ID(0))


def test_stop_aborted_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.aborted)]
    show_service = show_service_create(shows, [], [], [], [], [], [], [], [])
    with pytest.raises(StopShowStatusError):
        show_service.stop(ID(0))


def test_stop_notallusersscored_error():
    shows = [mocked_showschema(id=1, status=ShowStatus.started)]  # show's id=1 => all_users_scored returns False
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, usershows, [], [], [], [], [])
    with pytest.raises(StopNotAllUsersScoredError):
        show_service.stop(ID(1))


def test_stop_ok():
    shows = [mocked_showschema(id=0, status=ShowStatus.started)]  # show's id=0 => all_users_scored returns False
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, usershows, [], [], [], [], [])
    show_service.stop(ID(0))


def test_register_animal_started_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.started)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    show_service = show_service_create(shows, [], [], [], [], animals, [], [], [])
    with pytest.raises(RegisterShowStatusError):
        show_service.register_animal(ID(0), ID(0))


def test_register_animal_stopped_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.stopped)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    show_service = show_service_create(shows, [], [], [], [], animals, [], [], [])
    with pytest.raises(RegisterShowStatusError):
        show_service.register_animal(ID(0), ID(0))


def test_register_animal_aborted_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.aborted)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    show_service = show_service_create(shows, [], [], [], [], animals, [], [], [])
    with pytest.raises(RegisterShowStatusError):
        show_service.register_animal(ID(0), ID(0))


def test_register_animal_multibreed_wrongspecies_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created, species_id=0, is_multi_breed=True, breed_id=None, standard_id=None)]
    breeds = [mocked_breedschema(id=0, species_id=1)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    show_service = show_service_create(shows, [], [], [], [], animals, [], breeds, [])
    with pytest.raises(RegisterAnimalCheckError):
        show_service.register_animal(animal_id=ID(0), show_id=ID(0))


def test_register_animal_singlebreed_wrongbreed_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created, species_id=None, is_multi_breed=False, breed_id=0, standard_id=0)]
    breeds = [mocked_breedschema(id=0, species_id=1), mocked_breedschema(id=1, species_id=1)]
    standards = [mocked_standardschema(0, 0, 100, 100, 100, False, False, 10, 10, 10)]
    animals = [mocked_animalschema(0, 0, 1, 100, 100, 100, False, False)]
    show_service = show_service_create(shows, [], [], [], [], animals, [], breeds, standards)
    with pytest.raises(RegisterAnimalCheckError):
        show_service.register_animal(animal_id=ID(0), show_id=ID(0))


def test_register_animal_singlebreed_checkanimal_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created, species_id=None, is_multi_breed=False, breed_id=0, standard_id=1)]
    breeds = [mocked_breedschema(id=0, species_id=1)]
    standards = [mocked_standardschema(1, 0, 100, 100, 100, False, False, 10, 10, 10)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, True, False)]
    show_service = show_service_create(shows, [], [], [], [], animals, [], breeds, standards)
    with pytest.raises(RegisterAnimalCheckError):
        show_service.register_animal(animal_id=ID(0), show_id=ID(0))


def test_register_animal_registered_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created, species_id=None, is_multi_breed=False, breed_id=0, standard_id=0)]
    breeds = [mocked_breedschema(id=0, species_id=1)]
    standards = [mocked_standardschema(0, 0, 100, 100, 100, False, False, 10, 10, 10)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, [], [], animals, [], breeds, standards)
    with pytest.raises(RegisterAnimalRegisteredError):
        show_service.register_animal(animal_id=ID(0), show_id=ID(0))


def test_register_animal_registered_ok():
    shows = [mocked_showschema(id=0, status=ShowStatus.created, species_id=None, is_multi_breed=False, breed_id=0, standard_id=0)]
    breeds = [mocked_breedschema(id=0, species_id=1)]
    standards = [mocked_standardschema(0, 0, 100, 100, 100, False, False, 10, 10, 10)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    animalshows = []
    show_service = show_service_create(shows, [], animalshows, [], [], animals, [], breeds, standards)
    assert show_service.register_animal(animal_id=ID(0), show_id=ID(0)).status == ShowRegisterAnimalStatus.register_ok


def test_register_user_started_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.started)]
    users = [mocked_userschema(0, UserRole.judge)]
    show_service = show_service_create(shows, [], [], [], [], [], users, [], [])
    with pytest.raises(RegisterShowStatusError):
        show_service.register_user(ID(0), ID(0))


def test_register_user_stopped_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.stopped)]
    users = [mocked_userschema(0, UserRole.judge)]
    show_service = show_service_create(shows, [], [], [], [], [], users, [], [])
    with pytest.raises(RegisterShowStatusError):
        show_service.register_user(ID(0), ID(0))


def test_register_user_aborted_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.aborted)]
    users = [mocked_userschema(0, UserRole.judge)]
    show_service = show_service_create(shows, [], [], [], [], [], users, [], [])
    with pytest.raises(RegisterShowStatusError):
        show_service.register_user(ID(0), ID(0))


def test_register_user_admin_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    users = [mocked_userschema(0, UserRole.admin)]
    show_service = show_service_create(shows, [], [], [], [], [], users, [], [])
    with pytest.raises(RegisterUserRoleError):
        show_service.register_user(ID(0), ID(0))


def test_register_user_guest_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    users = [mocked_userschema(0, UserRole.guest)]
    show_service = show_service_create(shows, [], [], [], [], [], users, [], [])
    with pytest.raises(RegisterUserRoleError):
        show_service.register_user(ID(0), ID(0))


def test_register_user_breeder_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    users = [mocked_userschema(0, UserRole.breeder)]
    show_service = show_service_create(shows, [], [], [], [], [], users, [], [])
    with pytest.raises(RegisterUserRoleError):
        show_service.register_user(ID(0), ID(0))


def test_register_user_registered_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    users = [mocked_userschema(0, UserRole.judge)]
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], [], usershows, [], [], users, [], [])
    with pytest.raises(RegisterUserRegisteredError):
        show_service.register_user(ID(0), ID(0))


def test_register_user_ok():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    users = [mocked_userschema(0, UserRole.judge)]
    usershows = []
    show_service = show_service_create(shows, [], [], usershows, [], [], users, [], [])
    assert show_service.register_user(ID(0), ID(0)).status == ShowRegisterUserStatus.register_ok


def test_unregister_animal_stopped_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.stopped)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, [], [],  animals, [], [], [])
    with pytest.raises(UnregisterShowStatusError):
        show_service.unregister_animal(ID(0), ID(0))


def test_unregister_animal_aborted_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.aborted)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, [], [],  animals, [], [], [])
    with pytest.raises(UnregisterShowStatusError):
        show_service.unregister_animal(ID(0), ID(0))


def test_unregister_animal_started_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.started)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, [], [],  animals, [], [], [])
    with pytest.raises(UnregisterShowStatusError):
        show_service.unregister_animal(ID(0), ID(0))


def test_unregister_animal_notregistered_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    animalshows = []
    show_service = show_service_create(shows, [], animalshows, [], [],  animals, [], [], [])
    with pytest.raises(UnregisterAnimalNotRegisteredError):
        show_service.unregister_animal(ID(0), ID(0))


def test_unregister_animal_ok():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    animals = [mocked_animalschema(0, 0, 0, 100, 100, 100, False, False)]
    animalshows = [mocked_animalshowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], animalshows, [], [],  animals, [], [], [])
    assert show_service.unregister_animal(ID(0), ID(0)).status == ShowRegisterAnimalStatus.unregister_ok


def test_unregister_user_stopped_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.stopped)]
    users = [mocked_userschema(0, UserRole.judge)]
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], [], usershows, [], [], users, [], [])
    with pytest.raises(UnregisterShowStatusError):
        show_service.unregister_user(ID(0), ID(0))


def test_unregister_user_aborted_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.aborted)]
    users = [mocked_userschema(0, UserRole.judge)]
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], [], usershows, [], [], users, [], [])
    with pytest.raises(UnregisterShowStatusError):
        show_service.unregister_user(ID(0), ID(0))


def test_unregister_user_started_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.started)]
    users = [mocked_userschema(0, UserRole.judge)]
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], [], usershows, [], [], users, [], [])
    with pytest.raises(UnregisterShowStatusError):
        show_service.unregister_user(ID(0), ID(0))


def test_unregister_user_notregistered_error():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    users = [mocked_userschema(0, UserRole.judge)]
    usershows = []
    show_service = show_service_create(shows, [], [], usershows, [], [], users, [], [])
    with pytest.raises(UnregisterUserNotRegisteredError):
        show_service.unregister_user(ID(0), ID(0))


def test_unregister_user_ok():
    shows = [mocked_showschema(id=0, status=ShowStatus.created)]
    users = [mocked_userschema(0, UserRole.judge)]
    usershows = [mocked_usershowschema(0, 0, 0, False)]
    show_service = show_service_create(shows, [], [], usershows, [], [], users, [], [])
    assert show_service.unregister_user(ID(0), ID(0)).status == ShowRegisterAnimalStatus.unregister_ok
