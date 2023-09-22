import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic.command import upgrade
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope='session')
def postgres_url():
    with PostgresContainer("postgres:latest") as postgres:
        yield postgres.get_connection_url()


@pytest.fixture(scope='session')
def alembic_config(postgres_url):
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_config


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(alembic_config):
    upgrade(alembic_config, "head")


@pytest.fixture(scope='session')
def session_factory(postgres_url):
    engine = create_engine(postgres_url)
    return sessionmaker(engine)


@pytest.fixture()
def session(session_factory):
    with session_factory() as session_:
        yield session_
