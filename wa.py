import requests
from config import ACCESS_CODE, PHONE_ID

def send_message(user_id, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_CODE}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": user_id, "text": {"body": text}}
    requests.post(url, headers=headers, json=data)

def send_interactive_menu(user_id):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_CODE}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": user_id,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "👋 Welcome to onFinder! \n Select an option below to get started."},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "locate_bus", "title": "Locate the Bus"}},
                    {"type": "reply", "reply": {"id": "route_bus", "title": "Bus Route & Timings"}}
                ]
            }
        }
    }
    requests.post(url, headers=headers, json=payload)

