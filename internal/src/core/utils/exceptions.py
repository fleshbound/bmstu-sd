from typing import Any

from pydantic import NonNegativeInt

from core.show.schema.show import ShowStatus
from core.user.schema.user import UserRole
from core.utils.types import ID, Email


class ShowServiceError(Exception):
    def __init__(self, detail: Any) -> None:
        super().__init__(detail)


class RegisterShowStatusError(ShowServiceError):
    def __init__(self, show_id: ID, show_status: ShowStatus, detail: Any = None):
        super().__init__("improper show status: " if detail is None else detail + f"show_id={show_id.value}"
                         + f"status={show_status}")


class StartShowStatusError(ShowServiceError):
    def __init__(self, show_id: ID, show_status: ShowStatus, detail: Any = None):
        super().__init__("improper show status: " if detail is None else detail + f"show_id={show_id.value}"
                         + f"status={show_status}")


class AbortShowStatusError(ShowServiceError):
    def __init__(self, show_id: ID, show_status: ShowStatus, detail: Any = None):
        super().__init__("improper show status for abort: " if detail is None else detail + f"show_id={show_id.value}"
                         + f"status={show_status}")
        
        
class StopNotAllUsersScoredError(ShowServiceError):
    def __init__(self, show_id: ID, count: NonNegativeInt, detail: Any = None):
        super().__init__("not all users have scored yet: " if detail is None else detail + f"show_id={show_id.value}"
                         + f"count={count}")


class StopShowStatusError(ShowServiceError):
    def __init__(self, show_id: ID, show_status: ShowStatus, detail: Any = None):
        super().__init__("improper show status for stop: " if detail is None else detail + f"show_id={show_id.value}"
                         + f"status={show_status}")


class UpdateShowStatusError(ShowServiceError):
    def __init__(self, show_id: ID, show_status: ShowStatus, detail: Any = None):
        super().__init__("improper show status for update: " if detail is None else detail + f"show_id={show_id.value}"
                         + f"status={show_status}")

        
class StartShowZeroRecordsError(ShowServiceError):
    type: str

    def __init__(self, show_id: ID, type: str):
        self.type = type
        super().__init__(f"show has zero {type} registration records: show_id={show_id}")


class CreateShowMultiBreedError(ShowServiceError):
    property_name: str

    def __init__(self, property_name: str, detail: Any = None):
        super().__init__(f"invalid multi-breed show parameters: {property_name}"
                         + (": " + detail) if detail is not None else "")


class CreateShowSingleBreedError(ShowServiceError):
    property_name: str

    def __init__(self, property_name: str, detail: Any = None):
        super().__init__(f"invalid single-breed show parameters: {property_name}"
                         + (": " + detail) if detail is not None else "")


class UnregisterShowStatusError(ShowServiceError):
    def __init__(self, show_id: ID, show_status: ShowStatus, detail: Any = None):
        super().__init__("improper show status: " if detail is None else detail + f"show_id={show_id.value}"
                         + f"status={show_status}")


class RegisterAnimalCheckError(ShowServiceError):
    def __init__(self, show_id: ID, animal_id: ID, detail: Any = None):
        super().__init__(f'animal doesn\'t meet the show requirements: ' if detail is None else detail
                         + f"show_id={show_id.value}, animal_id={animal_id.value}")


class RegisterUserRoleError(ShowServiceError):
    def __init__(self, show_id: ID, user_id: ID, role: UserRole, detail: Any = None):
        super().__init__(f'user must be a judge: ' if detail is None else detail
                         + f"show_id={show_id.value}, user_id={user_id.value}, role={role}")


class RegisterAnimalRegisteredError(ShowServiceError):
    def __init__(self, show_id: ID, animal_id: ID, detail: Any = None):
        super().__init__(f'animal has been already registered: ' if detail is None else detail
                         + f"show_id={show_id.value}, animal_id={animal_id.value}")


class UnregisterAnimalNotRegisteredError(ShowServiceError):
    def __init__(self, show_id: ID, animal_id: ID, detail: Any = None):
        super().__init__(f'animal isn\'t registered to show: ' if detail is None else detail
                         + f"show_id={show_id.value}, animal_id={animal_id.value}")


class UnregisterUserNotRegisteredError(ShowServiceError):
    def __init__(self, show_id: ID, user_id: ID, detail: Any = None):
        super().__init__(f'animal isn\'t registered to show: ' if detail is None else detail
                         + f"show_id={show_id.value}, user_id={user_id.value}")


class RegisterUserRegisteredError(ShowServiceError):
    def __init__(self, show_id: ID, user_id: ID, detail: Any = None):
        super().__init__(f'user has been already registered: ' if detail is None else detail
                         + f"show_id={show_id.value}, user_id={user_id.value}")


class StandardServiceError(Exception):
    def __init__(self, detail: Any) -> None:
        super().__init__(detail)


class StandardInUseError(StandardServiceError):
    def __init__(self, standard_id: ID, detail: Any = None):
        super().__init__(f'standard is being used at some shows: ' if detail is None else detail
                         + f"standard_id={standard_id.value}")


class CheckAnimalStandardError(StandardServiceError):
    property_name: str

    def __init__(self, animal_id: ID, standard_id: ID, property_name: str = None, detail: Any = None):
        self.property_name = property_name
        super().__init__(f'animal check by standard error: {property_name}'
                         + (': ' + detail) if detail is not None else ""
                         + f"standard_id={standard_id.value}, animal_id={animal_id.value}")


class CheckAnimalBreedError(StandardServiceError):
    def __init__(self, animal_id: ID, standard_id: ID, detail: Any = None):
        super().__init__(f'improper animal breed_id: ' if detail is None else detail
                         + f"standard_id={standard_id.value}, animal_id={animal_id.value}")


class AuthServiceError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class SignInNotFoundEmailError(AuthServiceError):
    def __init__(self, email: Email):
        super().__init__(f'email not found: {email.value}')


class SignInPasswordError(AuthServiceError):
    def __init__(self, detail: Any = None):
        super().__init__(detail if detail else 'invalid password')


class AnimalServiceError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class UserServiceError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class EmailAlreadyTakenError(UserServiceError):
    def __init__(self, email: Email, detail: Any = None):
        super().__init__(detail if detail else f'email\'s already taken: email={email.value}')


class DeleteAnimalStartedShowError(AnimalServiceError):
    def __init__(self, animal_id: ID, detail: Any = None) -> None:
        super().__init__(detail if detail else f'animal is registered to started shows: animal_id={animal_id}')


class AnimalShowServiceError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class ScoreServiceError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class UserShowServiceError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class DuplicatedRepoError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class NotFoundRepoError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class TooManyResultsRepoError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)


class ValidationRepoError(Exception):
    def __init__(self, detail: Any = None) -> None:
        super().__init__(detail)
