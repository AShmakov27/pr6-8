import asyncio
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from app import rabbitmq
from app.settings import settings
from app.endpoints.student_router import student_router, metrics_router


app = FastAPI(title='Attendance Service')

instrumentator= Instrumentator()
instrumentator.instrument(app).expose(app)

@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(metrics_router)
app.include_router(student_router, prefix='/api')
