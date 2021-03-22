import logging
from json import decoder
from typing import Union

import requests
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, relationship

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('__name__')

engine = create_engine('sqlite:///logs.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Logs(object):
    def __init__(self, log):
        self.created_at = log['created_at']
        self.message = log['message']
        self.user_id = log['user_id']


class Users(object):
    def __init__(self, log):
        self.first_name = log['first_name']
        self.second_name = log['second_name']
        self.user_id = log['user_id']


class Errors(object):
    def __init__(self, log):
        self.error = log['error']


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    second_name = Column(String)
    log = relationship('Log', back_populates='user')


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    created_at = Column(Integer, nullable=False, index=True)
    message = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='log')


class Error(Base):
    __tablename__ = 'error'

    id = Column(Integer, primary_key=True)
    error = Column(String, nullable=False, index=True)


Base.metadata.create_all(engine)


class GetLog:
    """Getting logs from a third-party resource,
    processing them, and saving them to a local database."""

    def get(self, date: Union[int, str]) -> dict:
        """Gets log."""
        logs_get = requests.get(f'http://www.dsdev.tech/logs/{date}')
        return logs_get.json()

    def sort_date(self, logs: list) -> list:
        """Sorts logs by record creation date."""
        length = len(logs)
        if length > 2:
            part_1 = self.sort_date(logs[:length // 2])
            part_2 = self.sort_date(logs[length // 2:])
            logs = part_1 + part_2
            last_index = len(logs) - 1
            for i in range(last_index):
                min_value = logs[i]['created_at']
                min_index = i
                for j in range(i + 1, last_index + 1):
                    if min_value > logs[j]['created_at']:
                        min_value = logs[j]['created_at']
                        min_index = j

                if min_index != i:
                    logs[i], logs[min_index] = logs[min_index], logs[i]

                elif (len(logs) > 1 and
                      logs[0]['created_at'] > logs[1]['created_at']):
                    logs[0], logs[1] = logs[1], logs[0]
        return logs

    def saving_logs(self, data: dict) -> None:
        """Saves logs to the database."""
        if 'logs' in data:
            mapper(Logs, Log)
            mapper(Users, User)

            sorted_logs = get_log.sort_date(data['logs'])
            logger.debug('Произошел запуск функции sort_date()')
            logger.info('Логи отсортированы.')

            session.add_all([Users(i) for i in sorted_logs])
            session.add_all([Logs(i) for i in sorted_logs])
            logger.info('Логи в ожидании сохранения в БД.')

        else:
            mapper(Errors, Error)
            session.add(Errors(logs))
            logger.info('Логи с ошибкой в ожидании сохранения в БД.')
        session.commit()
        logger.info('Запись объектов в БД создана.')


if __name__ == "__main__":
    date = input()
    get_log = GetLog()
    try:
        logs = get_log.get(date)
        get_log.saving_logs(logs)
    except (
            requests.exceptions.RequestException,
            decoder.JSONDecodeError) as err:
        logger.error(err, exc_info=True)
