MESS_TIMINGS = {
    "breakfast": "7:00 AM - 9:00 AM",
    "lunch": "12:00 PM - 2:00 PM",
    "dinner": "7:00 PM - 9:00 PM"
}

MENU = {
    "breakfast": "Menu not configured",
    "lunch": "Menu not configured",
    "dinner": "Menu not configured"
}

SCHEMAS = {
    "get_mess_timing": {
        "type": "function",
        "function": {
            "name": "get_mess_timing",
            "description": "Get the timing for a college mess meal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "meal": {
                        "type": "string",
                        "enum": ["breakfast", "lunch", "dinner"],
                        "description": "The meal whose timing is requested."
                    }
                },
                "required": ["meal"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    "get_menu": {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Get the menu configured for a college mess meal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "meal": {
                        "type": "string",
                        "enum": ["breakfast", "lunch", "dinner"],
                        "description": "The meal whose menu is requested."
                    }
                },
                "required": ["meal"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
}


def get_mess_timing(meal):
    """Return the configured timing for a meal."""
    if meal not in MESS_TIMINGS:
        return "Error: Unknown meal."
    return MESS_TIMINGS[meal]


def get_menu(meal):
    """Return the configured menu for a meal."""
    if meal not in MENU:
        return "Error: Unknown meal."
    return MENU[meal]


TOOLS = {
    "get_mess_timing": get_mess_timing,
    "get_menu": get_menu
}
