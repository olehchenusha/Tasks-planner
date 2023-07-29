import asyncio
import database

from flask import Flask, render_template
from main import on_startup
from aiogram import executor
from bot import dp as main_dp
from create_bot import dp, bot, logger

app = Flask(__name__)

async def get_tasks():
    tasks = await database.get_all_tasks()
    return tasks


@app.route('/')
async def index():
    await database.start_db()
    tasks = await get_tasks()
    return render_template('index.html', tasks=tasks)


if __name__ == '__main__':
    asyncio.run(app.run(debug=True))