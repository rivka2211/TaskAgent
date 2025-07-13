toolsList = [
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "AGet all tasks from the list.",
            "parameters": {
                "additionalProperties": False
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a task to the list.",
            "parameters": {
                "type": "task",
                "additionalProperties": False
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_task",
            "description": "Remove a task from the list.",
            "parameters": {
                "type": "task",
                "additionalProperties": False
            },
            "strict": True,
        }
    }, {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update one task in the list.",
            "parameters": {
                "tasks": [
                    {
                        "name": "oldtask",
                        "type": "task",
                    },
                    {
                        "name": "newtask",
                        "type": "task",
                    }
                ],
                "additionalProperties": False
            },
            "strict": True,
        }
    },
    {
        "type": "object",
        "object": {
            "name": "task",
            "description": "The type of the task in this application.",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The unique code of the task."
                },
                "title": {
                    "type": "string",
                    "description": "The title of the task."
                },
                "description": {
                    "type": "string",
                    "description": "The description of the task (optional)."
                },
                "type": {
                    "type": "string",
                    "description": "The type of the task."
                },
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The start date of the task."
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The end date of the task (optional)."
                },
                "status": {
                    "type": "string",
                    "description": "The status of the task."
                }
            },
            "required": ["code", "title", "type", "start_date", "status"],
        },
        "strict": True,
    }
]
