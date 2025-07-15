from openai import OpenAI
import json
from todo_service import get_tasks, add_task, update_task, delete_task, load_all_tasks
from typing import Dict, Any
import os
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('MY_API_KEY')
client = OpenAI(api_key=api_key)

functions = [
    {
        "name": "add_task",
        "description": "הוספת משימה חדשה",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "כותרת המשימה"},
                "description": {"type": "string", "description": "תיאור המשימה"},
                "task_type": {
                    "type": "string",
                    "enum": ["פגישה", "עבודה", "שיחה", "למידה", "אישי", "חופשה", "תזכורת"],
                    "description": "סוג המשימה"
                },
                "start_date": {"type": "string", "description": "תאריך התחלה בפורמט ISO"},
                "end_date": {"type": "string", "description": "תאריך סיום בפורמט ISO"},
                "status": {
                    "type": "string",
                    "enum": ["מתוכננת", "בתהליך", "הושלמה", "בוטלה"],
                    "description": "סטטוס המשימה"
                }
            },
            "required": ["title", "task_type", "start_date", "status"]
        },
    },
    {
        "name": "get_tasks",
        "description": "שליפת משימות עם אפשרות סינון",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "סינון לפי סטטוס"},
                "task_type": {"type": "string", "description": "סינון לפי סוג משימה"},
                "start_date": {"type": "string", "description": "תאריך התחלה לסינון"},
                "end_date": {"type": "string", "description": "תאריך סיום לסינון"},
                "sort_by": {"type": "string", "enum": ["start_date", "title"], "description": "שדה למיון"},
                "sort_order": {"type": "string", "enum": ["asc", "desc"], "description": "סדר מיון"},
                "description": {"type": "string", "description": "חיפוש בתיאור"}
            }
        },
    },
    {
        "name": "update_task",
        "description": "עדכון משימה לפי כותרת",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "כותרת המשימה לעדכון"},
                "new_title": {"type": "string", "description": "כותרת חדשה"},
                "description": {"type": "string", "description": "תיאור חדש"},
                "task_type": {"type": "string", "description": "סוג משימה חדש"},
                "start_date": {"type": "string", "description": "תאריך התחלה חדש"},
                "end_date": {"type": "string", "description": "תאריך סיום חדש"},
                "status": {"type": "string", "description": "סטטוס חדש"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "delete_task",
        "description": "מחיקת משימה לפי כותרת",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "כותרת המשימה למחיקה"}
            },
            "required": ["title"]
        }
    }
]

system_prompt = f"""אתה עוזר אישי לניהול יומן ומשימות.
היום הוא: {datetime.now().strftime('%Y-%m-%d %H:%M')}

תפקידך: לנתח בקשות משתמשים ולהפעיל את הפונקציות המתאימות.

כללי המרה לתאריכים:
- "מחר" = {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}
- "ביום שני" = יום שני הקרוב
- "בשבוע הבא" = השבוע הבא
- אם לא צוין תאריך סיום, הוסף שעה אחת לתאריך התחלה

עבור update ו-delete, השתמש בכותרת המשימה לזיהוי.

דוגמאות:
- "תוסיף פגישה עם מיכל מחר בשעה 10" → add_task
- "מה יש לי השבוע?" → get_tasks עם טווח תאריכים
- "תמחק את הפגישה עם מיכל" → delete_task עם title
- "תשנה את הפגישה עם מיכל ליום שישי" → update_task
"""


def find_task_by_title(title: str):
    """חיפוש משימה לפי כותרת"""
    tasks = load_all_tasks()
    for task in tasks:
        if task["title"].lower() == title.lower():
            return task
    return None


def agent(query: str) -> str:
    try:
        print("🧠 שאלה מהמשתמש:", query)

        # שליחת השאלה ל־OpenAI עם פונקציות
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            functions=functions,
            function_call="auto"
        )

        message = response.choices[0].message
        print("📩 תשובת GPT:", message)

        # אם GPT בחר לקרוא לפונקציה
        if message.function_call:
            function_name = message.function_call.name
            arguments = json.loads(message.function_call.arguments)
            print(f"⚙ קורא לפונקציה: {function_name} עם ארגומנטים: {arguments}")

            if function_name == "add_task":
                # וודא שיש תיאור
                if "description" not in arguments:
                    arguments["description"] = ""
                result = add_task(**arguments)
                return f"✅ המשימה '{arguments['title']}' נוספה בהצלחה!\nמזהה: {result}"

            elif function_name == "get_tasks":
                result = get_tasks(**arguments)
                if not result:
                    return "📝 לא נמצאו משימות לפי הקריטריונים שלך"

                # עיצוב יפה של התוצאות
                response_text = f"📋 נמצאו {len(result)} משימות:\n\n"
                for i, task in enumerate(result, 1):
                    status_emoji = {"מתוכננת": "📅", "בתהליך": "⏳", "הושלמה": "✅", "בוטלה": "❌"}.get(task["status"],
                                                                                                    "📝")
                    response_text += f"{i}. {status_emoji} {task['title']}\n"
                    response_text += f"   📊 סטטוס: {task['status']}\n"
                    response_text += f"   🗓️ תאריך: {task['start_date']}\n"
                    if task.get("description"):
                        response_text += f"   📄 תיאור: {task['description']}\n"
                    response_text += "\n"

                return response_text.strip()

            elif function_name == "update_task":
                # מצא את המשימה לפי כותרת
                task = find_task_by_title(arguments["title"])
                if not task:
                    return f"❌ לא נמצאה משימה עם הכותרת '{arguments['title']}'"

                # הסר את ה-title מהארגומנטים ועדכן
                title_to_find = arguments.pop("title")
                if "new_title" in arguments:
                    arguments["title"] = arguments.pop("new_title")

                success = update_task(task["id"], **arguments)
                return f"✅ המשימה '{title_to_find}' עודכנה בהצלחה!" if success else "❌ שגיאה בעדכון המשימה"

            elif function_name == "delete_task":
                # מצא את המשימה לפי כותרת
                task = find_task_by_title(arguments["title"])
                if not task:
                    return f"❌ לא נמצאה משימה עם הכותרת '{arguments['title']}'"

                success = delete_task(task["id"])
                return f"🗑️ המשימה '{arguments['title']}' נמחקה בהצלחה!" if success else "❌ שגיאה במחיקת המשימה"
            else:
                return "⚠️ פונקציה לא נתמכת"

        else:
            # אם GPT לא בחר פונקציה, זה אומר שהוא לא הבין
            return "❓ לא הצלחתי להבין איזו פעולה לבצע. נסה לנסח את הבקשה אחרת.\n\nדוגמאות:\n• תוסיף פגישה עם יואב מחר בשעה 15\n• מה יש לי השבוע?\n• תמחק את הפגישה עם מיכל"

    except Exception as e:
        print(f"🚨 שגיאה: {str(e)}")
        return f"🚨 שגיאה: {str(e)}"


answer = agent("i need to sleape all this week")
print(answer)
