import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.settings import settings
from app.services.mark_service import MarkService
from app.repositories.db_student_repo import StudentRepo


async def process_created_student(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        MarkService(StudentRepo()).create_student(
            data['id'], data['FIO'])
    except:
        traceback.print_exc()
        await msg.ack()


async def process_satisfactory_student(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        MarkService(StudentRepo()).satisfactory_student(data['id'])
    except:
        await msg.ack()
    pass

async def process_good_student(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        MarkService(StudentRepo()).good_student(data['id'])
    except:
        await msg.ack()
    pass

async def process_excellent_student(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        MarkService(StudentRepo()).excellent_student(data['id'])
    except:
        await msg.ack()
    pass

async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    student_created_queue = await channel.declare_queue('shmakov_student_created_queue', durable=True)
    student_satisfactory_queue = await channel.declare_queue('shmakov_student_satisfactory_queue', durable=True)
    student_good_queue = await channel.declare_queue('shmakov_student_good_queue', durable=True)
    student_excellent_queue = await channel.declare_queue('shmakov_student_excellent_queue', durable=True)

    await student_created_queue.consume(process_created_student)
    await student_satisfactory_queue.consume(process_satisfactory_student)
    await student_good_queue.consume(process_good_student)
    await student_excellent_queue.consume(process_excellent_student)
    print('Started RabbitMQ consuming...')

    return connection
