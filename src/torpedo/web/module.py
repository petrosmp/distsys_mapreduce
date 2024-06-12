import os

import flask_injector
from injector import Binder, Module, inject
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from src.torpedo.repository import Repository


class TorpedoModule(Module):  # type:ignore[misc]
    def configure(self, binder: Binder) -> None:
        binder.bind(Engine, to=self.engine, scope=flask_injector.singleton)  # type: ignore[attr-defined]
        binder.bind(Repository, to=self.repository, scope=flask_injector.singleton)  # type: ignore[attr-defined]

    @inject
    def engine(self) -> Engine:
        """
        Creates and returns an `Engine` instance that handles DB operations.

        The `Engine` is connected with a postgres database described in the following
        environment variables:
            - POSTGRES_USERNAME
            - POSTGRES_PASSWORD
            - POSTGRES_HOST
            - POSTGRES_DB
        Port is 5432 by default. psycopg is used to connect to the db.
        """
        pg_user = os.environ.get("POSTGRES_USERNAME", "")
        pg_pass = os.environ.get("POSTGRES_PASSWORD", "")
        pg_host = os.environ.get("POSTGRES_HOST", "")
        pg_name = os.environ.get("POSTGRES_DB", "")
        db_url = f"postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:5432/{pg_name}"  # noqa: E231
        return create_engine(db_url)

    @inject
    def repository(self, engine: Engine) -> Repository:
        """Creates and returns a `Repository` instance that allows for persistent storage operations."""
        Session = sessionmaker(bind=engine)  # noqa: N806

        return Repository(Session)