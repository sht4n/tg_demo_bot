from fastapi import APIRouter, Depends
from typing import Annotated

from repository import FormRepository
from schema import SForm, SFormId, SFormUserId, SFormStatus, SFeed


router = APIRouter(
    prefix="/form",
)

@router.post("/upload")
async def load_form(
    form: Annotated[SForm, Depends()]
) -> SFormId:
    form_id = await FormRepository.upload_form(data=form)
    return {"id": form_id}

@router.get("/check")
async def check_form(
    user_id: Annotated[SFormUserId, Depends()]
) -> SFormStatus:
    is_existed = await FormRepository.check_form(data=user_id)
    return {"is_existed": is_existed}

@router.get("/get_candidates")
async def get_feed(
    user_id: Annotated[SFormUserId, Depends()]
) -> SFeed:
    forms = await FormRepository.get_candidates(data=user_id)
    return {"feed": forms}