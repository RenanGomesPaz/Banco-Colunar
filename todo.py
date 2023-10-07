import uuid
from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster(['localhost'])
session = cluster.connect('todolist')

# Create the tasks table if it doesn't exist
session.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id UUID PRIMARY KEY,
        title TEXT,
        description TEXT
    )
""")

def add_task(title, description):
    # Generate a unique ID for the task
    task_id = uuid.uuid4()
    # Insert the task into the database
    session.execute("""
        INSERT INTO tasks (id, title, description)
        VALUES (%s, %s, %s)
    """, (task_id, title, description))

def list_tasks():
    # Retrieve and display all tasks
    rows = session.execute("SELECT id, title FROM tasks")
    for row in rows:
        print('Task ID: {}, Title: {}'.format(row.id, row.title))

def view_task_description(task_id):
    # Retrieve and display the description of a specific task
    row = session.execute("SELECT description FROM tasks WHERE id = %s", [task_id]).one()
    if row:
        print('Task Description:', row.description)
    else:
        print('Task not found.')

def remove_task(task_id):
    # Remove a task from the database
    session.execute("DELETE FROM tasks WHERE id = %s", [task_id])
    print('Task removed.')

if __name__ == '__main__':
    while True:
        print('\nOptions:')
        print('1. Add Task')
        print('2. List Tasks')
        print('3. View Task Description')
        print('4. Remove Task')
        print('5. Quit')

        choice = raw_input('Enter your choice: ')

        if choice == '1':
            title = raw_input('Enter task title: ')
            description = raw_input('Enter task description: ')
            add_task(title, description)
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            task_id = raw_input('Enter task ID to view description: ')
            view_task_description(task_id)
        elif choice == '4':
            task_id = raw_input('Enter task ID to remove: ')
            remove_task(task_id)
        elif choice == '5':
            break
        else:
            print('Invalid choice. Please try again.')

# Close the Cassandra session and cluster when done
session.shutdown()
cluster.shutdown()