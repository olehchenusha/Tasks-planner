import datetime
import aiogram
import database

from create_bot import dp, bot, logger

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command



@dp.message_handler(commands=['start'], state='*')
async def start(message:types.Message, state: FSMContext):
    try:
        await state.finish()
    except:
        pass

    user = await database.get_user(message.from_user.id)

    if user is None:
        await database.create_user(
            message.from_user.id, message.from_user.username
        )

    await message.answer(f"Привiт! Завдяки цьому боту ти можеш створити список задач!\n\n"
                         f"Список команд:\n"
                         f"/tasks - виведе всi iснуючi задачi\n"
                         f"<code>/create_task 'Задача'</code> - створить задачу\n"
                         f"<code>/add_comment 'Номер задачi' 'Коментар'</code> - додасть до задачi коментар"
                         )
    
@dp.message_handler(commands=['tasks'], state='*')
async def tasks(message:types.Message, state: FSMContext):
    all_tasks = await database.get_all_tasks()

    if len(all_tasks) != 0:
        msg = 'Всi задачi:'
        for task in all_tasks:
            msg = f"{msg}\n{task['id']} - {task['task_name']}"

        await message.answer(f"{msg}\n\nСтворити задачу - <code>/create_task 'Задача'</code>\nДодати коментар - <code>/add_comment 'Номер задачi' 'Коментар'</code>")
    else:
        await message.answer(f"Список задач пустий\n\nСтворити задачу - <code>/create_task 'Задача'</code>\nДодати коментар - <code>/add_comment 'Номер задачi' 'Коментар'</code>")
    

@dp.message_handler(regexp=r'^/create_task\s+[\s\S]+', state='*')
async def create_task(message:types.Message, state: FSMContext):
    try:
        task_name = message.text.split(' ', 1)[1:]
    except Exception as e:
        logger.error(f'Введено некоректну назву: {e}')

    if len(task_name) == 0:
        await message.answer('Введiть коректну назву')
        return
    
    max_id = await database.get_max_task()

    if max_id == None:
        id = 1
    else:
        id = max_id+1

    date = datetime.datetime.now()
    date = date.strftime('%Y-%m-%d %H-%M-%S')

    await database.create_task(id, task_name[0], date, '[]')

    await message.answer(f'Задачу створено пiд номером {id}')

@dp.message_handler(Command('create_task'))
async def empty_task(message:types.Message, state: FSMContext):
    await message.answer('Назва не може бути пустою. Використовуйте <code>/create_task ЗАДАЧА</code>')

@dp.message_handler(regexp=r'^/add_comment\s+\d+\s+[\s\S]+', state='*')
async def add_comment(message:types.Message, state: FSMContext):
    task_id, message_text = message.text.split(" ", 2)[1:]

    task = await database.get_task(int(task_id))

    if task is None:
        await message.answer('Задачi з таким номером не iснує')
        return

    comment = task["comment"]
    comment = eval(comment)

    if len(comment) == 0:
        new_comment = str([message_text])
    else:
        new_comment = f'["{comment[0]}", "{message_text}"]'

    await database.update_comment(int(task_id), new_comment)
    
    await message.answer(f"В задачу {task_id} був додан коментар {message_text}")