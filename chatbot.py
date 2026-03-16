import json
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from auth_db import register_user, login_user, save_summary, generate_summary


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load dataset
with open("mental_awareness_60_trees_kb.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# Keep only ROOT nodes
roots = [node for node in data if node.get("type") == "root"]


# Root embeddings
root_vectors = np.array([node["vector"] for node in roots])


# Groq LLM
llm = ChatGroq(
    temperature=0.3,
    max_tokens=120,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


# Distress detection
def detect_distress(text):

    distress_keywords = [
        "can't handle","hopeless","crying","suicidal","hurt myself",
        "depressed","anxious","can't stop crying","losing control",
        "breaking down","self harm","cut myself","want to die",
        "kill myself","end my life","no way out","i give up",
        "i can't go on","nothing will get better","suicide",
        "worthless","alone"
    ]

    text = text.lower()

    for word in distress_keywords:
        if word in text:
            return True

    return False


# Find best root
def find_best_root(user_input):

    query_vec = model.encode(user_input)

    similarities = np.dot(root_vectors, query_vec)

    best_index = np.argmax(similarities)

    best_score = similarities[best_index]

    return roots[best_index], best_score


# Groq short response
def groq_answer(question):

    prompt = f"""
You are a mental wellness chatbot.

Rules:
- Respond in maximum 2 sentences
- Be supportive and empathetic
- Keep answers short

User message:
{question}
"""

    response = llm.invoke(prompt)

    return response.content


print("\n🧠 Mental Wellness Chatbot")


# STEP 9 — LOGIN / REGISTER
print("1. Register")
print("2. Login")

choice = input("Choose option: ")

if choice == "1" or choice == "register":
    register_user()

user_id = login_user()

print("\nType 'exit' to stop\n")


current_tree = None
followup_index = 0
conversation_history = []


while True:

    user_input = input("You: ")

    conversation_history.append("User: " + user_input)

    print("DEBUG user_id:", user_id)
    # EXIT → SAVE SUMMARY
    if user_input.lower() == "exit":

        summary = generate_summary(llm, conversation_history)

        save_summary(user_id, summary)

        print("Bot: Chat summary saved. Take care!")

        break


    # Distress detection
    if detect_distress(user_input):

        bot_msg = "It sounds like you're going through something really difficult. Please contact support: +91 8840209873"

        print("\nBot:", bot_msg)

        conversation_history.append("Bot: " + bot_msg)

        current_tree = None
        followup_index = 0
        continue


    # FOLLOW-UP HANDLING
    if current_tree:

        word_count = len(user_input.split())

        # Short answer → continue follow-up
        if word_count < 3:

            followups = current_tree.get("followups", [])

            bot_msg = followups[followup_index]["answer"]

            print("\nBot:", bot_msg)

            conversation_history.append("Bot: " + bot_msg)

            followup_index += 1

            if followup_index < len(followups):

                bot_msg = followups[followup_index]["question"]

                print("\nBot:", bot_msg)

                conversation_history.append("Bot: " + bot_msg)

            else:

                bot_msg = "Thank you for sharing. If you'd like to talk about something else, feel free to tell me."

                print("\nBot:", bot_msg)

                conversation_history.append("Bot: " + bot_msg)

                current_tree = None
                followup_index = 0

            continue


        # Longer message → similarity routing
        best_root, followup_score = find_best_root(user_input)


        # RAG
        if followup_score >= 0.6:

            current_tree = best_root
            followup_index = 0

            bot_msg = current_tree["response"]

            print("\nBot:", bot_msg)

            conversation_history.append("Bot: " + bot_msg)

            if current_tree["followups"]:

                bot_msg = current_tree["followups"][0]["question"]

                print("\nBot:", bot_msg)

                conversation_history.append("Bot: " + bot_msg)

            continue


        # GROQ
        elif 0.3 <= followup_score < 0.6:

            response = groq_answer(user_input)

            print("\nBot:", response)

            conversation_history.append("Bot: " + response)

            current_tree = None
            followup_index = 0

            continue


        # AGENT
        else:

            bot_msg = "I'm not able to help with this question. Please contact support: +91 8840209873"

            print("\nBot:", bot_msg)

            conversation_history.append("Bot: " + bot_msg)

            current_tree = None
            followup_index = 0

            continue


    # NORMAL QUERY ROUTING
    best_root, score = find_best_root(user_input)


    # RAG
    if score > 0.6:

        current_tree = best_root
        followup_index = 0

        bot_msg = current_tree["response"]

        print("\nBot:", bot_msg)

        conversation_history.append("Bot: " + bot_msg)

        if current_tree["followups"]:

            bot_msg = current_tree["followups"][0]["question"]

            print("\nBot:", bot_msg)

            conversation_history.append("Bot: " + bot_msg)

        continue


    # GROQ
    elif 0.3 <= score <= 0.6:

        response = groq_answer(user_input)

        print("\nBot:", response)

        conversation_history.append("Bot: " + response)

        continue


    # AGENT
    else:

        bot_msg = "I'm not confident about this question. Please contact support: +91 8840209873"

        print("\nBot:", bot_msg)

        conversation_history.append("Bot: " + bot_msg)

        continue