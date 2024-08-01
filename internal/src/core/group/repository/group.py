from abc import abstractmethod
from typing import List

from pydantic import NonNegativeInt

from core.group.schema.group import GroupSchema
from utils.repository.base import IBaseRepository


class IGroupRepository(IBaseRepository):
    pass
