import requests
from pydantic import BaseModel
from typing import Optional
from config import N8N_WEBHOOK_URL


class LeadInput(BaseModel):
    name: str
    email: str
    contact: Optional[str] = "N/A"
    service: Optional[str] = "N/A"
    budget: Optional[str] = "Not provided"
    company: Optional[str] = "N/A"
    project_summary: Optional[str] = "N/A"
    integrations: Optional[str] = "N/A"
    timeline: Optional[str] = "N/A"
    existing_software: Optional[str] = "N/A"
    conversation_summary: Optional[str] = "N/A"

def create_lead_tool(input_data: LeadInput):
    # Convert data into dictionary
    payload = input_data.dict()
    
    try:
        # Timeout (10 seconds)
        res = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        
        # Status code 200 or 201 (Created)
        if res.status_code in [200, 201]:
            return "Thank you! Your details have been successfully captured. Our team will contact you shortly." 
        else:
            return f"Server responded with an error. Status code: {res.status_code}"
            
    except requests.exceptions.Timeout:
        return "Error: The connection to our server timed out. Please try again later."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the server." 
        return f"An unexpected error occurred: {str(e)}"