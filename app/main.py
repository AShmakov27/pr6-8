import asyncio
from fastapi import FastAPI

from app import rabbitmq
from app.settings import settings
from app.endpoints.student_router import student_router


app = FastAPI(title='Delivery Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(student_router, prefix='/api')
