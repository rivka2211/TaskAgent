# from datetime import datetime, timedelta
# from http import client
#
# import requests
# import json
# import tools
# from tools import toolsList
#
# # OpenAI API key configuration
# import os
# from dotenv import load_dotenv
#
# # טען את המפתחות הסודיים מתוך הקובץ .env
# load_dotenv()
#
# # גש למפתחות הסודיים
# api_key = os.getenv('MY_API_KEY')
# url = os.getenv('MY_URL')
#
# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }
# system_prompt = f"""אתה עוזר אישי לניהול יומן ומשימות.
# היום הוא: {datetime.now().strftime('%Y-%m-%d %H:%M')}
#
# תפקידך: לנתח בקשות משתמשים ולהפעיל את הפונקציות המתאימות.
#
# כללי המרה לתאריכים:
# - "מחר" = {(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}
# - "ביום שני" = יום שני הקרוב
# - "בשבוע הבא" = השבוע הבא
# - אם לא צוין תאריך סיום, הוסף שעה אחת לתאריך התחלה
#
# עבור update ו-delete, השתמש בכותרת המשימה לזיהוי.
#
# דוגמאות:
# - "תוסיף פגישה עם מיכל מחר בשעה 10" → add_task
# - "מה יש לי השבוע?" → get_tasks עם טווח תאריכים
# - "תמחק את הפגישה עם מיכל" → delete_task עם title
# - "תשנה את הפגישה עם מיכל ליום שישי" → update_task
# """
#
# async def agent(query: str):
#     print("in openai_chat_completion")
#     messages = [{"role":"system","content":system_prompt},{"role": "user", "content": query}]
#     print(type(toolsList))
#     try:
#         # response = requests.post(url, headers=headers, json={
#         #     "model": "gpt-4o-mini",
#         #     "messages": messages,
#         #     # "tools": toolsList,
#         #     # "tool_choice": "required"
#         # })
#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": query}
#             ],
#             functions=toolsList,
#             function_call="auto"
#         )
#         print("after the request to openai")
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.HTTPError as http_err:
#         return None
#
#     #  completion = response.json()
#     # print(completion)
#     #
#     # tool_call = completion['choices'][0]['message']['tool_calls'][0]
#     # args = json.loads(tool_call['function']['arguments'])
#     #
#     # result = get_weather(args["latitude"], args["longitude"])
#     #
#     # messages.append(completion['choices'][0]['message'])  # append model's function call message
#     # messages.append({  # append result message
#     #     "role": "tool",
#     #     "tool_call_id": tool_call['id'],
#     #     "content": result
#     # })
#     #
#     # try:
#     #     response2 = requests.post(url, headers=headers, json={
#     #         "model": "gpt-4o-mini",
#     #         "messages": messages,
#     #         "tools": tools
#     #     })
#     #     response2.raise_for_status()
#     # except requests.exceptions.HTTPError as http_err:
#     #     return None
#     #
#     # return response2.json()
#
# # toolsList = [
# #     {
# #         "type": "function",
# #         "function": {
# #             "name": "get_tasks",
# #             "description": "AGet all tasks from the list.",
# #             "parameters": {
# #                 "additionalProperties": False
# #             },
# #             "strict": True,
# #         }
# #     },
# #     {
# #         "type": "function",
# #         "function": {
# #             "name": "add_task",
# #             "description": "Add a task to the list.",
# #             "parameters": {
# #                 "type": "task",
# #                 "additionalProperties": False
# #             },
# #             "strict": True,
# #         }
# #     },
# #     {
# #         "type": "function",
# #         "function": {
# #             "name": "remove_task",
# #             "description": "Remove a task from the list.",
# #             "parameters": {
# #                 "type": "task",
# #                 "additionalProperties": False
# #             },
# #             "strict": True,
# #         }
# #     }, {
# #         "type": "function",
# #         "function": {
# #             "name": "update_task",
# #             "description": "Update one task in the list.",
# #             "parameters": {
# #                 "tasks": [
# #                     {
# #                         "name": "oldtask",
# #                         "type": "task",
# #                     },
# #                     {
# #                         "name": "newtask",
# #                         "type": "task",
# #                     }
# #                 ],
# #                 "additionalProperties": False
# #             },
# #             "strict": True,
# #         }
# #     },
# #     {
# #         "type": "object",
# #         "object": {
# #             "name": "task",
# #             "description": "The type of the task in this application.",
# #             "properties": {
# #                 "code": {
# #                     "type": "string",
# #                     "description": "The unique code of the task."
# #                 },
# #                 "title": {
# #                     "type": "string",
# #                     "description": "The title of the task."
# #                 },
# #                 "description": {
# #                     "type": "string",
# #                     "description": "The description of the task (optional)."
# #                 },
# #                 "type": {
# #                     "type": "string",
# #                     "description": "The type of the task."
# #                 },
# #                 "start_date": {
# #                     "type": "string",
# #                     "format": "date",
# #                     "description": "The start date of the task."
# #                 },
# #                 "end_date": {
# #                     "type": "string",
# #                     "format": "date",
# #                     "description": "The end date of the task (optional)."
# #                 },
# #                 "status": {
# #                     "type": "string",
# #                     "description": "The status of the task."
# #                 }
# #             },
# #             "required": ["code", "title", "type", "start_date", "status"],
# #         },
# #         "strict": True,
# #     }
# # ]
