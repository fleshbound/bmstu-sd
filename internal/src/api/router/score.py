from typing import List, Union

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status, APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import NonNegativeInt, PositiveInt

from container.container import Container
from core.show.schema.score import ScoreSchemaCreate, ScoreSchema, ScoreSchemaUpdate
from core.show.service.score import IScoreService
from core.utils.exceptions import ValidationRepoError
from core.utils.types import ID

router = APIRouter(
    prefix="/score",
    tags=["Score"]
)

dep_score = Depends(Provide[Container.score_service])


@router.post("")
@inject
def create_score(
        score_create: ScoreSchemaCreate,
        score_service: IScoreService = dep_score
) -> ScoreSchema:
    try:
        res = score_service.create(score_create)
    except ValidationRepoError as e:
        return PlainTextResponse(f'error: {str(e)}')
    return res
