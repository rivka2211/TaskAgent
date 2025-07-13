tasks = []


def get_tasks():
    return tasks


def add_task(task):
    tasks.append(task)


def remove_task(task):
    if (task in tasks):
        tasks.remove(task)


def update_task(oldtask, newtask):
    if (oldtask in tasks):
        tasks.remove(oldtask)
    tasks.append(newtask)
