from typing import Any, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCharityRepository
from app.models import CharityProject


class CRUDCharityproject(BaseCharityRepository):
    """Репозиторий для управления благотворительными проектами."""

    def __init__(self):
        """Инициализирует DonationRepository с заданной моделью."""
        super().__init__(CharityProject)

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        """Получает идентификатор проекта по имени."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_keywords(
        self,
        session: AsyncSession,
        **kwargs: Any
    ) -> List[CharityProject]:
        """Получает проекты по произвольным ключевым аргументам."""
        query = select(CharityProject)

        for key, value in kwargs.items():
            if hasattr(CharityProject, key):
                query = query.where(getattr(CharityProject, key) == value)

        result = await session.execute(query)
        return result.scalars().all()

    async def get_project_by_completion_rate(
        self,
        session: AsyncSession
    ) -> List[tuple]:
        """Получает проекты с их скоростью завершения."""
        projects = await session.execute(
            select(
                CharityProject.name,
                (
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                ).label('date_difference'),
                CharityProject.description
            ).where(
                CharityProject.fully_invested
            ).order_by('date_difference')
        )
        return projects.all()


charity_project_crud = CRUDCharityproject()
