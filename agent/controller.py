import json
from openai import OpenAI
from agent.prompt import SYSTEM_PROMPT
from config import OPENAI_API_KEY 

from tools.rag_tool import rag_search_tool, RAGInput
from tools.lead_tool import create_lead_tool, LeadInput
from tools.service_tool import get_service_info_tool, ServiceInput

client = OpenAI(api_key=OPENAI_API_KEY)

# Updated run_agent to accept history (conversation memory)
def run_agent(user_message: str, history: list = None):
    if history is None:
        history = []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        response_format={"type": "json_object"},
        timeout=30  # <--- YEH LINE ADD KAREIN
    )
    return json.loads(response.choices[0].message.content)

# Updated agent_controller to accept and pass history
def agent_controller(user_message: str, history: list = None):
    agent_output = run_agent(user_message, history)

    # Sometimes LLM might miss the action or tool_input in JSON, so we use .get() safely
    action = agent_output.get("action", "None")
    tool_input = agent_output.get("tool_input", {})

    # Handle the Human-in-the-Loop confirmation response
    if action == "None" or action == "confirm_lead":
        return {"message": agent_output.get("final_answer", "Please provide more details.")}

    # Execute the requested tools
    if action == "rag_search":
        return rag_search_tool(RAGInput(**tool_input))
    
    if action == "create_lead":
        return create_lead_tool(LeadInput(**tool_input))

    if action == "get_service_info":
        return get_service_info_tool(ServiceInput(**tool_input))

    # Fallback if no tool is called
    return {"message": agent_output.get("final_answer", "I am not sure how to help with that.")}