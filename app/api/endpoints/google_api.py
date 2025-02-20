from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project
from app.services.google_api import (add_user_permissions, create_spreadsheet,
                                     update_spreadsheet_value)

router = APIRouter()


@router.post(
    '/google',
    response_model=list,
    dependencies=[Depends(current_superuser)],
    summary='Создание Google таблицы'
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """Создает отчет в виде Google таблицы, добавляет информацию о проектах."""
    project = await charity_project.get_project_by_complection_rate(session)
    spreadsheetid = await create_spreadsheet(wrapper_services)
    await add_user_permissions(spreadsheetid, wrapper_services)
    await update_spreadsheet_value(spreadsheetid,
                                   project,
                                   wrapper_services)
    return project
