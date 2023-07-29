import asyncio
import asyncpg

from create_bot import DB_NAME, DB_HOST, DB_PASS, DB_USER

async def start_db() -> None:
    global pool
    pool = await asyncpg.create_pool(database=DB_NAME, user=DB_USER,
                                     password=DB_PASS, host=DB_HOST)
    
    async with pool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS users("
                           "id bigint PRIMARY KEY, "
                           "username TEXT)")
        
        await conn.execute("CREATE TABLE IF NOT EXISTS tasks("
                           "id int PRIMARY KEY, "
                           "task_name TEXT,"
                           "create_date TEXT,"
                           "comment TEXT)")

    
async def create_user(id, username) -> None:
    try:
        async with pool.acquire() as conn:
            await conn.execute("INSERT INTO users(id,username) VALUES($1,$2)", 
                               int(id),username)
    except Exception as ex:
        print(f'Error in database.create_user: {ex}')

async def create_task(id, task_name, date, comment) -> None:
    try:
        async with pool.acquire() as conn:
            await conn.execute("INSERT INTO tasks(id,task_name,create_date,comment) VALUES($1,$2,$3,$4)", 
                               int(id), task_name, date, comment)
    except Exception as ex:
        print(f'Error in database.create_task: {ex}')

async def get_user(id) -> []:
    async with pool.acquire() as conn:
        data = await conn.fetchrow("SELECT * FROM users WHERE id = $1", id)
        return data
    
async def get_task(id) -> []:
    async with pool.acquire() as conn:
        data = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", id)
        return data
    
async def get_max_task() -> int:
    async with pool.acquire() as conn:
        data = await conn.fetchval("SELECT max(id) FROM tasks")
        return data
    
async def get_all_tasks() -> []:
    async with pool.acquire() as conn:
        data = await conn.fetch("SELECT * FROM tasks")
        return data
    
async def update_comment(id, comment):
    try:
        async with pool.acquire() as conn:
            await conn.execute("UPDATE tasks SET comment = $1 WHERE id = $2", 
                               comment, int(id))
    except Exception as ex:
        print(f'Error in database.update_comment: {ex}')