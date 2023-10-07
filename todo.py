from cassandra.cluster import Cluster
from uuid import uuid4

cluster = Cluster(['localhost'])
session = cluster.connect('todolist') 

def add_task(title, description):
    task_id = uuid4()
    session.execute("""
        INSERT INTO tasks (task_id, title, description)
        VALUES (%s, %s, %s)
    """, (task_id, title, description))

def list_tasks():
    rows = session.execute('SELECT task_id, title FROM tasks')
    for row in rows:
        print(f'Task ID: {row.task_id}, Title: {row.title}')

def view_task_description(task_id):
    row = session.execute('SELECT description FROM tasks WHERE task_id = %s', [task_id]).one()
    if row:
        print(f'Task Description: {row.description}')
    else:
        print('Task not found.')

def remove_task(task_id):
    session.execute('DELETE FROM tasks WHERE task_id = %s', [task_id])

add_task('Task 1', 'Description of Task 1')
add_task('Task 2', 'Description of Task 2')
list_tasks()
view_task_description(task_id)
remove_task(task_id)