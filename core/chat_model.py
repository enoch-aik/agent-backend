# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/openai/


from dotenv import load_dotenv
from google.cloud import firestore
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_openai import ChatOpenAI
from prompts import technicalPrototypePrompt

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

# Firebase Firestore - save conversation history
PROJECT_ID = "game-startup-ai-agent"
SESSION_ID = "dev_session" 
COLLECTION_NAME = "chat_history"

print("Initializing Firestore Client...")
client = firestore.Client(project=PROJECT_ID)


# Initialize Firestore Chat Message History
print("Initializing Firestore Chat Message History...")
chat_history = FirestoreChatMessageHistory(
    session_id=SESSION_ID,
    collection=COLLECTION_NAME,
    client=client,
)

#print all messages in the chat history
messages = chat_history.messages
for message in messages:
    print(f"Type: {message.type}, Content: {message.content}")


# # Create the chat prompt template for mock game reviews
# template = "I am an Indie game developer working on developing a side " \
# "scroller game and based on previous game reviews, what do people not " \
# "like about {topic}."
# prompt_template = ChatPromptTemplate.from_messages(technicalPrototypePrompt)
# print(str(prompt_template.invoke))

# Extra Informoation about Part 3.
# This does work:
messages = [
    ("system", "You are {agent}."),    

]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"agent": technicalPrototypePrompt})
# print(prompt)
chat_history.add_user_message(str(prompt))

result = model.invoke(prompt)

# Add response to chat history
chat_history.add_ai_message(str(result.content))
print(result.content)
# prompt = prompt_template.invoke({"topic": "side-scroller games"})
# #add prompt to chat history

# chat_history.add_user_message(str(prompt))
# result = model.invoke(prompt)

# #add response to chat history
# chat_history.add_ai_message(str(result.content))

# print(result.content)

# while True:
#     human_input = input("User: ")
#     if human_input.lower() == "exit":
#         break

#     chat_history.add_user_message(human_input)

#     ai_response = model.invoke(chat_history.messages)
#     chat_history.add_ai_message(str(ai_response.content))

#     print(f"AI: {ai_response.content}")