from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from setup.web import create_app
from setup.ioc import create_container


def make_app() -> FastAPI:
    app = create_app()
    container = create_container()
    setup_dishka(container=container, app=app)

    return app


app = make_app()
