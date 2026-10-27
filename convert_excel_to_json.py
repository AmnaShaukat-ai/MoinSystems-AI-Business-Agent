import pandas as pd

df = pd.read_excel("MoinSystems_AI_Public_Chatbot_RAG_Dataset_v2 (1).xlsx")
df.to_json("MoinSystems_services.json", orient = "index", indent = 4)