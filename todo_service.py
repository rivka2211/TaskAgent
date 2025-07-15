from datetime import datetime

# דוגמת רשימת משימות
tasks = [
    {"title": "Task 1", "status": "completed", "task_type": "type1", "start_date": "2023-01-01",
     "end_date": "2023-01-10", "description": "First task"},
    {"title": "Task 2", "status": "pending", "task_type": "type2", "start_date": "2023-01-05", "end_date": "2023-01-15",
     "description": "Second task"},
    {"title": "Task 3", "status": "completed", "task_type": "type1", "start_date": "2023-01-10",
     "end_date": "2023-01-20", "description": "Third task"},
]


def get_tasks(status=None, task_type=None, start_date=None, end_date=None, sort_by=None, sort_order='asc',description=None):
    filtered_tasks = tasks

    # סינון לפי סטטוס
    if status:
        filtered_tasks = [task for task in filtered_tasks if task['status'] == status]

    # סינון לפי סוג משימה
    if task_type:
        filtered_tasks = [task for task in filtered_tasks if task['task_type'] == task_type]

    # סינון לפי תאריכים
    if start_date:
        filtered_tasks = [task for task in filtered_tasks if
                          datetime.strptime(task['start_date'], "%Y-%m-%d") >= datetime.strptime(start_date,
                                                                                                 "%Y-%m-%d")]

    if end_date:
        filtered_tasks = [task for task in filtered_tasks if
                          datetime.strptime(task['end_date'], "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d")]

    # סינון לפי תיאור
    if description:
        filtered_tasks = [task for task in filtered_tasks if description.lower() in task['description'].lower()]

    # מיון
    if sort_by:
        filtered_tasks.sort(key=lambda x: x[sort_by], reverse=(sort_order == 'desc'))

    return filtered_tasks


def add_task(title, description, task_type, start_date, end_date, status):
    # בדיקה אם כל הפרמטרים הנדרשים נמסרו
    if not title or not task_type or not start_date or not status:
        raise ValueError("כל הפרמטרים הנדרשים חייבים להיות מסופקים")

    # יצירת משימה חדשה
    new_task = {
        "title": title,
        "description": description,
        "task_type": task_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": status
    }

    # הוספת המשימה לרשימה
    tasks.append(new_task)
    return new_task


def delete_task(title):
    global tasks
    tasks = [task for task in tasks if task['title'] != title]


def update_task(title, new_title=None, description=None, task_type=None, start_date=None, end_date=None, status=None):
    for task in tasks:
        if task['title'] == title:
            if new_title:
                task['title'] = new_title
            if description:
                task['description'] = description
            if task_type:
                task['task_type'] = task_type
            if start_date:
                task['start_date'] = start_date
            if end_date:
                task['end_date'] = end_date
            if status:
                task['status'] = status
            return task
    return None  # אם לא נמצאה משימה עם הכותרת

def load_all_tasks():
    global tasks
    return tasks