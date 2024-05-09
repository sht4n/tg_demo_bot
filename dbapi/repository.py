from datetime import datetime, UTC
from sqlalchemy import select

from database import async_session
from models import FormsOrm
from schema import SForm, SFormUserId


class FormRepository:
    @classmethod
    async def upload_form(cls, data: SForm) -> int:
        async with async_session() as session:
            form_dict = data.model_dump()
            form = FormsOrm(**form_dict)
            session.add(form)
            await session.flush()
            await session.commit()
            return form.form_id

    @classmethod
    async def check_form(cls, data: SFormUserId) -> bool:
        async with async_session() as session:
            query = select(FormsOrm).where(
                FormsOrm.user_id == data.user_id
            )
            result = await session.execute(query)
            is_existed = result.one_or_none() is not None
            return is_existed

    @classmethod    
    async def get_candidates(cls, data: SFormUserId) -> list[SForm] | None:
        async with async_session() as session:
            query = select(FormsOrm).where(
                FormsOrm.user_id == data.user_id
            )
            result = await session.execute(query)
            form = result.scalar_one_or_none()
            if form is None:
                return None
            query = select(FormsOrm).where(
                FormsOrm.preference == form.preference
                and FormsOrm.goal == form.goal
                and FormsOrm.user_id != form.user_id
            )
            result = await session.execute(query)
            feed = result.scalars()
            return feed


            