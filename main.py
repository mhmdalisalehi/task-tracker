import os
import json
import argparse

TASKS_FILE = 'tasks.json'

def load():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def save(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add(tasks, title):
    tasks.append({'id': len(tasks) + 1, 'title': title, 'status': 'not done'})
    save(tasks)
    print("Task added.\n")

def update(tasks, id, title):
    for task in tasks:
        if task['id'] == id:
            task['title'] = title
            save(tasks)
            print(f"Task {id} updated.\n")
            return
    print(f"Task with ID {id} not found.\n")

def delete(tasks, id):
    task_to_delete = None
    for task in tasks:
        if task['id'] == id:
            task_to_delete = task
            break

    if task_to_delete:
        tasks.remove(task_to_delete)
        save(tasks)
        print(f"Task with ID {id} deleted.\n")
    else:
        print(f"Task with ID {id} not found.\n")

def list_tasks(tasks, status=None):
    for task in tasks:
        if status is None or task['status'] == status:
            print(f"{task['id']}. {task['title']} [{task['status']}]")

def mark_in_progress(tasks, id):
    for task in tasks:
        if task['id'] == id:
            if task['status'] == 'not done':
                task['status'] = 'in progress'
                save(tasks)
                print(f"Task {id} marked as in progress.\n")
                return
            elif task['status'] == 'done':
                print("Task is already done.\n")
                return
            elif task['status'] == 'in progress':
                print("Task is already in progress.\n")
                return
    print(f"Task with ID {id} not found.\n")

def mark_done(tasks, id):
    for task in tasks:
        if task['id'] == id:
            if task['status'] in ['not done', 'in progress']:
                task['status'] = 'done'
                save(tasks)
                print(f"Task {id} marked as done.\n")
                return
            elif task['status'] == 'done':
                print("Task is already done.\n")
                return
    print(f"Task with ID {id} not found.\n")

def mark_not_done(tasks, id):
    for task in tasks:
        if task['id'] == id:
            if task['status'] in ['done', 'in progress']:
                task['status'] = 'not done'
                save(tasks)
                print(f"Task {id} marked as not done.\n")
                return
            elif task['status'] == 'not done':
                print("Task is already not done.\n")
                return
    print(f"Task with ID {id} not found.\n")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument("action", choices=['add', 'list', 'update', 'delete', 'mark_in_progress', 'mark_done', 'mark_not_done'], help="Action to perform")
    parser.add_argument('--title', help="Title of the task (for 'add' and 'update' actions)")
    parser.add_argument('--id', type=int, help="ID of the task (for 'update', 'delete', 'mark_in_progress', 'mark_done', and 'mark_not_done' actions)")
    parser.add_argument('--status', choices=['done', 'not done', 'in progress'], help="Status filter for 'list' action")

    args = parser.parse_args()
    tasks = load()

    if args.action == 'add' and args.title:
        add(tasks, args.title)
    elif args.action == 'list':
        list_tasks(tasks, args.status)
    elif args.action == 'update' and args.id and args.title:
        update(tasks, args.id, args.title)
    elif args.action == 'delete' and args.id:
        delete(tasks, args.id)
    elif args.action == 'mark_in_progress' and args.id:
        mark_in_progress(tasks, args.id)
    elif args.action == 'mark_done' and args.id:
        mark_done(tasks, args.id)
    elif args.action == 'mark_not_done' and args.id:
        mark_not_done(tasks, args.id)
    else:
        print("Invalid command or missing arguments.\n")

if __name__ == "__main__":
    main()
