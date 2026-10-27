import json
from pydantic import BaseModel

class ServiceInput(BaseModel):
    service_name: str

def get_service_info_tool(input_data: ServiceInput):
    with open("data/moinsystems_services.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    user_query = input_data.service_name.lower()

    for item in data.values():
        title = item.get("Title", "").lower()
        intents = item.get("Intents", "").lower()

        # Match company info
        if "company" in user_query or "email" in user_query or "website" in user_query:
            if "company_info" in intents or "contact" in intents:
                return {
                    "title": item.get("Title"),
                    "info": item.get("Content")
                }

        # Match services
        if user_query in title or user_query in intents.replace("_", " "):
            return {
                "service": item.get("Title"),
                "description": item.get("Content"),
                "note": "Pricing depends on project scope. The chatbot must not guarantee a fixed price."
            }

    return {"error": "Service not found"}
