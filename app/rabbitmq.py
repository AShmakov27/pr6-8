import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.settings import settings
from app.services.attendance_service import AttendanceService
from app.repositories.db_student_repo import StudentRepo


async def process_created_student(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        AttendanceService(StudentRepo()).create_student(
            data['id'], data['FIO'])
    except:
        traceback.print_exc()
        await msg.ack()


async def process_attend_student(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        AttendanceService(StudentRepo()).attend_student(data['id'])
    except:
        await msg.ack()
    pass


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    student_created_queue = await channel.declare_queue('shmakov_student_created_queue', durable=True)
    student_attend_queue = await channel.declare_queue('shmakov_student_attend_queue', durable=True)

    await student_created_queue.consume(process_created_student)
    await student_attend_queue.consume(process_attend_student)
    print('Started RabbitMQ consuming...')

    return connection
