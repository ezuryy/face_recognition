from fastapi import Depends
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from datetime import date, datetime, timedelta
import os

from working_time_system.db.models import WorkTime
from working_time_system.db.connection import get_session


events_folder_path = f'database_with_events'


class WorkTimeRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def write_event_to_csv(self, name: str, event_type: str):
        now = datetime.now()
        now_date = now.strftime('%Y-%m-%d')
        events_file_path = events_folder_path + f'/events_{now_date}.csv'
        if not os.path.isfile(events_file_path):
            start_df = pd.DataFrame({'time': [], 'name': [], 'event_type': []})
            start_df.to_csv(events_file_path, index=False)

        df = pd.read_csv(events_file_path)
        dt_from = now - timedelta(minutes=5)
        updated_df = df.copy()
        updated_df = updated_df[updated_df.name == name]
        updated_df['time'] = pd.to_datetime(updated_df['time'])
        updated_df = updated_df[updated_df.time > dt_from]
        if updated_df.shape[0] == 0:
            print(f'Write to file {event_type} of {name}')
            df = pd.concat([df, pd.DataFrame({'time': [now], 'name': [name], 'event_type': [event_type]})])
            df.to_csv(events_file_path, index=False)

            if event_type == 'entrance':
                await self._init_working_hours(name)
            elif event_type == 'exit':
                # TODO: check that type of last event of current person was 'entrance', else - write error to log
                df = df[df.name == name]
                df = df[df.event_type == 'entrance']
                df = df.sort_values('time')
                last_entrance_time = pd.to_datetime(df['time'].values[-1])
                diff = now - last_entrance_time
                work_hours = round(diff.seconds / 3600, 2)
                print(f'diff = {diff}')
                await self._update_working_hours(name, work_hours)

    async def _init_working_hours(self, name: str):
        print('init_working_hours')
        query = await self._session.execute(
            select(WorkTime).where((WorkTime.name == name) & (func.DATE(WorkTime.date) == date.today()))
        )
        entry = query.scalars().all()

        if len(entry) == 0:
            print('creating working_hours in db...')
            query = insert(WorkTime).values(date=date.today(), name=name, work_hours=0)
            await self._session.execute(query)
            await self._session.commit()


    async def _update_working_hours(self, name: str, work_hours: float):
        print('update_working_hours')
        query = await self._session.execute(
            select(WorkTime).where((WorkTime.name == name) & (func.DATE(WorkTime.date) == date.today()))
        )
        entry = query.scalars().first()
        entry.work_hours += work_hours
        await self._session.commit()


async def get_work_time_repository(session: AsyncSession = Depends(get_session)) -> WorkTimeRepository:
    return WorkTimeRepository(session=session)
